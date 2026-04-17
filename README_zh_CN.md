[English](README.md)

# 导出到飞书

一个将思源笔记文档导出到飞书文档的插件。**由Claude Code编写**。

## 功能特性

- **一键导出**：通过顶栏按钮或快捷键，一键将当前文档导出到飞书文档
- **文件夹选择**：每次导出时可选择飞书云空间中的目标文件夹
- **导出历史追踪**：自动在文档属性中记录导出历史
- **重复导出检测**：导出已导出过的文档时会弹出确认提示
- **转换状态反馈**：实时显示上传和转换进度
- **错误处理**：显示来自飞书 API 的详细错误信息和警告

## 安装

### ~~从集市安装~~
并没有上架


### 手动安装

1. 从 [Releases](https://github.com/yourusername/export-to-feishu/releases) 下载 `package.zip`
2. 解压到 `{思源工作空间}/data/plugins/export-to-feishu/`
3. 重启思源或重新加载插件

## 配置

使用插件前，需要配置飞书 API 访问权限：

### 1. 获取飞书 Access Token

你需要从飞书开放平台获取 `tenant_access_token` 或 `user_access_token`。

> **注意：** `tenant_access_token` 代表应用/企业租户身份调用 API。使用它导出的文档可能归属于应用或企业空间，导致在个人飞书账号的「我的空间」中**无法查看**。普通用户强烈建议改用 **`user_access_token`**，这样文档会出现在你的个人云空间中。

#### 适合普通用户的方法

1. 访问 [API 调试台](https://open.feishu.cn/api-explorer/)
2. 点击获取Token
3. 登录飞书授权
4. 将获取到的`user_access_token` 复制
5. 完事

#### 正规方法

如果你想创建自己的飞书应用并在本地获取 `user_access_token`，可以使用仓库中提供的辅助脚本：

1. 在 [飞书开放平台](https://open.feishu.cn/app) 创建自定义应用，并启用 **"网页应用"** 登录功能。
2. 设置重定向 URL 为 `http://localhost:8080/callback`。
3. 记录你的 **App ID** 和 **App Secret**。
4. 运行辅助脚本 `scripts/get_feishu_user_token.py`：

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
python scripts/get_feishu_user_token.py
```

或者直接通过命令行参数传入：

```bash
python scripts/get_feishu_user_token.py --app-id your_app_id --app-secret your_app_secret
```

5. 脚本会自动打开浏览器进行授权。授权成功后，`user_access_token` 会打印在终端中。

#### 刷新已过期/即将过期的 Token

如果你之前获取到的 `refresh_token` 仍然有效，可以通过以下方式直接刷新 `user_access_token`，无需再次打开浏览器授权：

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
python scripts/refresh_feishu_user_token.py --refresh-token "your_refresh_token"
```

或者直接传入参数：

```bash
python scripts/refresh_feishu_user_token.py --refresh-token "your_refresh_token" --app-id your_app_id --app-secret your_app_secret
```

### 2. 配置插件

1. 打开思源笔记 → 设置 → 插件 → 导出到飞书
2. 输入飞书 Access Token
3. 点击「选择」按钮选择临时文件上传目录
   - 该目录用于转换过程中临时存放 Markdown 文件
   - 转换成功后文件会自动删除

## 使用方法

### 导出文档

1. 在思源笔记中打开要导出的文档
2. 点击顶栏的飞书图标，或使用快捷键：
   - macOS: `Shift + Cmd + F`
   - Windows/Linux: `Shift + Ctrl + F`
3. 在弹窗中选择飞书云空间的目标文件夹
4. 点击「确定导出」开始导出

### 导出流程

```
思源文档 → Markdown → 上传到飞书 → 转换为飞书文档 → 清理临时文件
```

1. 通过思源 API 将文档导出为 Markdown
2. 将 Markdown 文件上传到飞书云空间的临时目录
3. 飞书将 Markdown 转换为飞书文档，保存到你选择的目标文件夹
4. 自动删除临时文件
5. 将飞书文档 token 保存到思源文档的属性中

### 重复导出

当导出一个之前已经导出过的文档时：
- 会弹出确认对话框
- 选择继续将会创建一个**新的**飞书文档（不会影响已有的文档）

## 从源码构建

### 环境要求

- [Node.js](https://nodejs.org/) (v16+)
- [pnpm](https://pnpm.io/)

### 命令

```bash
# 安装依赖
pnpm install

# 开发构建（监听模式）
pnpm run dev

# 生产构建（生成 package.zip）
pnpm run build

# 代码检查
pnpm run lint
```

开发时，将项目文件夹放置在 `{思源工作空间}/data/plugins/export-to-feishu/` 下可实现热重载。

## 限制

- 文档中的图片以 Markdown 图片链接形式导出
- 部分复杂的 Markdown 格式可能无法完美转换为飞书格式
- 飞书有内容限制：
  - 最多 20,000 个内容块
  - 最多 2,000 个表格单元格
  - 最多 100 列表格
  - 单段落最多 100,000 个 UTF-16 字符

## 常见问题

**Q: 为什么需要临时文件夹？**

A: 飞书的导入 API 需要先上传文件，再进行转换。临时文件夹用于存放转换过程中的 Markdown 文件，转换完成后会自动清理。

**Q: 可以替换/更新已有的飞书文档吗？**

A: 目前插件只支持创建新文档。替换/更新功能可能会在后续版本中添加。

**Q: 转换超时怎么办？**

A: 插件每 2 秒轮询一次转换状态，最多轮询 5 次（共 10 秒）。如果超时，会提示你手动前往飞书客户端确认结果。

**Q: 为什么使用 tenant_access_token 导出后在个人飞书空间里找不到文档？**

A: `tenant_access_token` 是以应用/企业租户的身份创建文档，文档可能归属于企业空间或应用空间，不会自动出现在你的个人云空间中。改用 `user_access_token` 即可让文档进入你的个人账号下。

**Q: 导出历史保存在哪里？**

A: 飞书文档的 token 保存在思源文档的自定义属性 `custom-feishu-doc-token` 中。

## 许可证

MIT
