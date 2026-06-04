#!/bin/sh
set -e

REPO_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
BACKEND_PORT="${BACKEND_PORT:-8001}"

echo "服务启动中："
echo "- 后端 + 前端（静态服务）：http://127.0.0.1:${BACKEND_PORT}/"
echo "- 项目分析页：            http://127.0.0.1:${BACKEND_PORT}/analysis"

cd "$REPO_ROOT"
exec python3 "$REPO_ROOT/backend/dev_server.py" --port "$BACKEND_PORT"
