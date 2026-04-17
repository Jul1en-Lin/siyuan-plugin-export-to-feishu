import argparse
import json
import os

import requests


def refresh_user_access_token(refresh_token, app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    resp = requests.post(url, json=payload, timeout=30)
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="刷新飞书 user_access_token")
    parser.add_argument("--refresh-token", required=True, help="之前获取到的 refresh_token")
    parser.add_argument("--app-id", help="飞书 App ID（也可通过环境变量 FEISHU_APP_ID 设置）")
    parser.add_argument("--app-secret", help="飞书 App Secret（也可通过环境变量 FEISHU_APP_SECRET 设置）")
    args = parser.parse_args()

    app_id = args.app_id or os.environ.get("FEISHU_APP_ID", "")
    app_secret = args.app_secret or os.environ.get("FEISHU_APP_SECRET", "")

    if not app_id or not app_secret:
        print("错误：请提供 app_id 和 app_secret")
        print("方式一：通过环境变量设置")
        print("  export FEISHU_APP_ID='your_app_id'")
        print("  export FEISHU_APP_SECRET='your_app_secret'")
        print("方式二：通过命令行参数传入")
        print("  python refresh_feishu_user_token.py --refresh-token xxx --app-id your_app_id --app-secret your_app_secret")
        return

    print("=" * 50)
    print("飞书 user_access_token 刷新工具")
    print("=" * 50)
    print("正在调用飞书 API 刷新 token...")

    result = refresh_user_access_token(args.refresh_token, app_id, app_secret)

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
        print("刷新成功！")
        print("=" * 50)
        print(f"user_access_token:  {token}")
        print(f"refresh_token:      {refresh}")
        print(f"expires_in:         {expire} 秒")
    else:
        print(f"\n刷新失败: {result.get('msg')} (code: {result.get('code')})")


if __name__ == "__main__":
    main()
