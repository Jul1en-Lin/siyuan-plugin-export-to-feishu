[中文](README_zh_CN.md)

# Export to Feishu

A SiYuan Note plugin that exports documents to Feishu (Lark) Docs. **Vibe coded by Claude Code**

## Features

- **One-click Export**: Export the current document to Feishu Docs via top bar button or shortcut
- **Folder Selection**: Choose the target folder in Feishu Drive for each export
- **Export History Tracking**: Automatically records export history in document attributes
- **Re-export Detection**: Warns when exporting a previously exported document
- **Conversion Status**: Real-time feedback on upload and conversion progress
- **Error Handling**: Displays detailed error messages and warnings from Feishu API

## Installation

### ~~From Marketplace~~


### Manual Installation

1. Download `package.zip` from [Releases](https://github.com/yourusername/export-to-feishu/releases)
2. Extract to `{SiYuan workspace}/data/plugins/export-to-feishu/`
3. Restart SiYuan or reload plugins

## Configuration

Before using the plugin, you need to configure the Feishu API access:

### 1. Get Feishu Access Token

You need a `tenant_access_token` or `user_access_token` from Feishu Open Platform.

> **Note:** `tenant_access_token` operates on behalf of the app/tenant. Documents created with it may be owned by the app or enterprise space, which can make them invisible in your personal Feishu account. For regular users, **`user_access_token`** is strongly recommended because documents will appear in your personal drive.

#### Easy Method for Regular Users

1. Visit [API Explorer](https://open.feishu.cn/api-explorer/)
2. Click "Get Token"
3. Login and authorize with Feishu
4. Copy the `user_access_token`
5. Done

#### Standard Method

If you prefer to create your own Feishu app and obtain a `user_access_token` locally, you can use the provided helper script:

1. Create a custom app in [Feishu Open Platform](https://open.feishu.cn/app) and enable **"Web application"** login.
2. Set the redirect URL to `http://localhost:8080/callback`.
3. Note down your **App ID** and **App Secret**.
4. Run the helper script in `scripts/get_feishu_user_token.py`:

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
python scripts/get_feishu_user_token.py
```

Or pass the credentials directly:

```bash
python scripts/get_feishu_user_token.py --app-id your_app_id --app-secret your_app_secret
```

5. The script will open your browser for authorization. After you approve it, the `user_access_token` will be printed in the terminal.

#### Refreshing an Expired Token

If your `user_access_token` is about to expire, you can use the `refresh_token` obtained earlier to get a new one without going through the browser authorization again:

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
python scripts/refresh_feishu_user_token.py --refresh-token "your_refresh_token"
```

Or pass credentials directly:

```bash
python scripts/refresh_feishu_user_token.py --refresh-token "your_refresh_token" --app-id your_app_id --app-secret your_app_secret
```

### 2. Configure the Plugin

1. Open SiYuan → Settings → Plugins → Export to Feishu
2. Enter your Feishu Access Token
3. Click "Select" to choose a temporary folder for file uploads
   - This folder is used to temporarily store markdown files during conversion
   - Files are automatically deleted after successful conversion

## Usage

### Export a Document

1. Open the document you want to export in SiYuan
2. Click the Feishu icon in the top bar, or use shortcut:
   - macOS: `Shift + Cmd + F`
   - Windows/Linux: `Shift + Ctrl + F`
3. Select the target folder in Feishu Drive
4. Click "Export" to start

### Export Flow

```
SiYuan Document → Markdown → Upload to Feishu → Convert to Feishu Doc → Cleanup
```

1. Document is exported as Markdown via SiYuan API
2. Markdown file is uploaded to the temporary folder in Feishu Drive
3. Feishu converts the Markdown to a Feishu Doc in your selected folder
4. Temporary file is automatically deleted
5. The Feishu Doc token is saved to the SiYuan document's attributes

### Re-exporting

When you export a document that has been exported before:
- A confirmation dialog will appear
- Choosing to continue will create a **new** Feishu Doc (the existing one is not affected)

## Build from Source

### Prerequisites

- [Node.js](https://nodejs.org/) (v16+)
- [pnpm](https://pnpm.io/)

### Commands

```bash
# Install dependencies
pnpm install

# Development build (with watch mode)
pnpm run dev

# Production build (generates package.zip)
pnpm run build

# Lint code
pnpm run lint
```

For development, place the project folder in `{SiYuan workspace}/data/plugins/export-to-feishu/` for live reload.

## Limitations

- Images in documents are exported as Markdown image links
- Some complex Markdown features may not convert perfectly to Feishu format
- Feishu has content limits:
  - Max 20,000 content blocks
  - Max 2,000 table cells
  - Max 100 table columns
  - Max 100,000 UTF-16 characters per paragraph

## FAQ

**Q: Why do I need a temporary folder?**

A: Feishu's import API requires uploading a file first, then converting it. The temporary folder stores the Markdown file during this process. It's automatically cleaned up after conversion.

**Q: Can I replace/update an existing Feishu Doc?**

A: Currently, the plugin only creates new documents. Update/replace functionality may be added in future versions.

**Q: What happens if conversion takes too long?**

A: The plugin polls for conversion status every 2 seconds, up to 5 times (10 seconds total). If it times out, you'll be prompted to check the result manually in Feishu.

**Q: Why can't I find the exported document in my personal Feishu space?**

A: If you used a `tenant_access_token`, the document is created on behalf of the app/tenant and may be located in the enterprise or app-owned space rather than your personal drive. Switch to a `user_access_token` to ensure documents appear under your personal account.

**Q: Where is the export history stored?**

A: The Feishu document token is stored in the SiYuan document's custom attribute `custom-feishu-doc-token`.

## License

MIT
