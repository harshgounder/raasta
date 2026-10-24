#!/usr/bin/env bash
# start (or restart) the reports service on :8790. Logs to data/server.log. Usage: ./run.sh [stop]
cd "$(dirname "$0")"
mkdir -p data
if [ -f data/server.pid ] && kill -0 "$(cat data/server.pid)" 2>/dev/null; then kill "$(cat data/server.pid)"; sleep 1; fi
[ "$1" = "stop" ] && exit 0
nohup .venv/bin/uvicorn server:app --host "${REPORTS_HOST:-127.0.0.1}" --port "${REPORTS_PORT:-8790}" >> data/server.log 2>&1 &
echo $! > data/server.pid
for i in $(seq 1 20); do curl -s -m 2 "http://127.0.0.1:${REPORTS_PORT:-8790}/health" >/dev/null && { echo "reports up on :${REPORTS_PORT:-8790}"; exit 0; }; sleep 0.5; done
echo "reports did not come up; see data/server.log"; exit 1
