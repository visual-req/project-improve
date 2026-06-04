# Troubleshooting

## 前端打不开 / 页面空白

- 确认通过仓库根目录启动静态服务（保证能读取 `work/` 目录）：

```bash
python3 -m http.server 5173 --bind 127.0.0.1
```

然后访问：

- `http://127.0.0.1:5173/frontend/`

## 报告加载失败（404）

- 确认报告路径符合约定：
  - `work/outputs/<project_id>/project-metrics-orid/report.json`
- 确认前端选择的 `project_id` 与输出目录一致

## Token 无效 / 拉取不到数据

- 确认环境变量名与 `work/meta/config.yaml` 中 `token_env` 一致
- 确认 token 权限覆盖所需 API（项目、Issue/PR、CI 运行记录、代码扫描结果等）

## npm/vite 无法运行（Node 版本不兼容）

如果你看到类似 “npm supports node ^20…” 的报错：

- 当前机器 Node 版本过低，无法运行新版本 npm/vite
- 解决方式：升级 Node 到 20+（例如使用 nvm），再在 `frontend/` 执行 `npm install && npm run dev`

## unpkg 资源加载失败

前端使用 CDN（unpkg）加载 Vue 与 Ant Design Vue：

- 确认网络可访问 unpkg
- 若公司网络屏蔽外链 CDN，建议改为本地安装依赖并使用 Vite 构建（见 Installation）
