# Demo video

页顶演示区使用单个视频文件：

- **`VT-WAM-Demo.mp4`** — 浏览器原生 controls，支持进度条跳转

## 编码要求

1. **faststart**：`moov` 元数据必须在文件头，否则浏览器无法快速 seek。

```powershell
ffmpeg -i VT-WAM-Demo.mp4 -c copy -movflags +faststart VT-WAM-Demo-fixed.mp4
```

2. **本地预览**：用仓库根目录的 `serve-local.ps1` 启动服务器，不要用 `python -m http.server`。

## 体积

当前约 47 MB。推送到 GitHub 前请确认未超过单文件限制；必要时使用 Git LFS。
