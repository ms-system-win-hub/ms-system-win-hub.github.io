# WAVFORM - FFmpeg Web 音频转换器

浏览器端音频转换工具，使用 FFmpeg.wasm，100% 本地处理。

## 功能

- 支持 MP3、WAV、FLAC、AAC、OGG、M4A 等格式转换为 MP3
- 无损格式自动使用高质量编码
- 支持 IndexedDB 缓存，第二次加载秒启动
- 纯前端，无需服务器

## 本地测试

```bash
cd /path/to/ffmpeg_web
python3 server.py
# 访问 http://localhost:8888
```

## 部署到 GitHub Pages

### 方法一：直接部署

1. 创建 GitHub 仓库
2. 上传所有文件到仓库
3. 在仓库 Settings → Pages → Source 选择 main 分支
4. 访问 `https://your-username.github.io/repo-name/`

**注意**：GitHub Pages 不支持自定义 HTTP 头，Service Worker 会自动注入 COOP/COEP 头。

### 方法二：使用 GitHub Actions（推荐）

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - uses: actions/deploy-pages@v4
        id: deployment
```

## 文件结构

```
ffmpeg_web/
├── index.html      # 主页面
├── sw.js           # Service Worker (COOP/COEP)
├── server.py       # 本地测试服务器
├── favicon.svg     # 网站图标
├── README.md       # 说明文档
└── ffmpeg/
    ├── ffmpeg-core.js      # FFmpeg 核心 JS
    ├── ffmpeg-core.wasm    # WebAssembly 二进制 (30MB)
    ├── dist/esm/           # FFmpeg ES 模块
    │   ├── index.js
    │   ├── classes.js
    │   ├── worker.js
    │   └── ...
    └── util/dist/esm/      # 工具函数
        ├── index.js
        └── ...
```

## 注意事项

1. **首次加载**：需要下载 30MB 的 wasm 文件，请耐心等待
2. **缓存**：加载完成后会缓存到 IndexedDB，下次秒开
3. **浏览器支持**：需要支持 SharedArrayBuffer 的现代浏览器（Chrome/Edge/Firefox/Safari 15.2+）

## License

MIT
