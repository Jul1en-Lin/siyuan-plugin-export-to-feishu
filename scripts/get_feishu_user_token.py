import argparse
import http.server
import json
import os
import socketserver
import threading
import urllib.parse
import webbrowser

import requests

# 配置
APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
REDIRECT_URI = "http://localhost:8080/callback"
PORT = 8080

auth_code = None
server_instance = None


class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code, server_instance
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/callback":
            code = params.get("code", [None])[0]

            if code:
                auth_code = code
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    "<h2>授权成功！请回到终端查看 user_access_token。</h2>".encode("utf-8")
                )

                def shutdown():
                    if server_instance:
                        server_instance.shutdown()

                threading.Thread(target=shutdown, daemon=True).start()
            else:
                error = params.get("error", ["unknown"])[0]
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h2>授权失败: {error}</h2>".encode("utf-8"))

                def shutdown():
                    if server_instance:
                        server_instance.shutdown()

                threading.Thread(target=shutdown, daemon=True).start()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def get_user_access_token(code, app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "app_id": app_id,
        "app_secret": app_secret,
    }
    resp = requests.post(url, json=payload, timeout=30)
    return resp.json()


def main():
    global server_instance

    parser = argparse.ArgumentParser(description="获取飞书 user_access_token")
    parser.add_argument("--app-id", help="飞书 App ID（也可通过环境变量 FEISHU_APP_ID 设置）")
    parser.add_argument("--app-secret", help="飞书 App Secret（也可通过环境变量 FEISHU_APP_SECRET 设置）")
    args = parser.parse_args()

    app_id = args.app_id or APP_ID
    app_secret = args.app_secret or APP_SECRET

    if not app_id or not app_secret:
        print("错误：请提供 app_id 和 app_secret")
        print("方式一：通过环境变量设置")
        print("  export FEISHU_APP_ID='your_app_id'")
        print("  export FEISHU_APP_SECRET='your_app_secret'")
        print("方式二：通过命令行参数传入")
        print("  python get_feishu_user_token.py --app-id your_app_id --app-secret your_app_secret")
        return

    auth_url = (
        f"https://open.feishu.cn/open-apis/authen/v1/index?"
        f"app_id={app_id}&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}&state=RANDOM_STATE"
    )

    print("=" * 50)
    print("飞书 user_access_token 获取工具")
    print("=" * 50)
    print(f"1. 正在启动本地回调服务器: {REDIRECT_URI}")

    with socketserver.TCPServer(("", PORT), CallbackHandler) as httpd:
        server_instance = httpd
        print(f"2. 回调服务器已启动，监听端口 {PORT}")
        print(f"3. 正在打开浏览器进行授权...\n")
        print(f"   如果浏览器没有自动打开，请手动访问:\n   {auth_url}\n")

        threading.Timer(1.0, lambda: webbrowser.open(auth_url)).start()
        httpd.serve_forever()

    if auth_code:
        print(f"\n4. 收到授权码 (auth_code): {auth_code}")
        print("5. 正在调用飞书 API 换取 user_access_token...")
        result = get_user_access_token(auth_code, app_id, app_secret)

        print("\n" + "=" * 50)
        print("API 响应结果:")
        print("=" * 50)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("code") == 0:
            data = result.get("data", {})
            token = data.get("access_token")
            refresh = data.get("refresh_token")
            expire = data.get("expires_in")
            print("\n" + "=" * 50)
            print("获取成功！")
            print("=" * 50)
            print(f"user_access_token:  {token}")
            print(f"refresh_token:      {refresh}")
            print(f"expires_in:         {expire} 秒")
        else:
            print(f"\n获取失败: {result.get('msg')} (code: {result.get('code')})")
    else:
        print("\n未能获取到授权码，流程中断。")


if __name__ == "__main__":
    main()
