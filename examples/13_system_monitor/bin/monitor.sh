#!/usr/bin/env bash
set -u
umask 0007

APP_NAME="${APP_NAME:-agent-app}"
APP_MATCH="${APP_MATCH:-agent-app|agent-app-linux-x86|agent-app-linux-arm64|agent_app.py}"
AGENT_HOME="${AGENT_HOME:-/opt/agent-app}"
AGENT_PORT="${AGENT_PORT:-15034}"
AGENT_LOG_DIR="${AGENT_LOG_DIR:-/var/log/agent-app}"
LOG_FILE="${MONITOR_LOG_FILE:-$AGENT_LOG_DIR/monitor.log}"
CPU_WARN="${CPU_WARN:-20}"
MEM_WARN="${MEM_WARN:-10}"
DISK_WARN="${DISK_WARN:-80}"
LOG_MAX_BYTES="${LOG_MAX_BYTES:-10485760}"
LOG_KEEP_COUNT="${LOG_KEEP_COUNT:-10}"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

log_line() {
  local level="$1"
  local message="$2"
  local line="[$(timestamp)] [$level] $message"
  echo "$line"
  printf "%s\n" "$line" >> "$LOG_FILE"
}

append_metric_line() {
  local pid="$1"
  local cpu="$2"
  local mem="$3"
  local disk="$4"
  local line="[$(timestamp)] PID:${pid} CPU:${cpu}% MEM:${mem}% DISK_USED:${disk}%"
  echo "$line"
  printf "%s\n" "$line" >> "$LOG_FILE"
}

ensure_log_file() {
  if [ ! -d "$AGENT_LOG_DIR" ]; then
    echo "[$(timestamp)] [ERROR] log directory not found: $AGENT_LOG_DIR" >&2
    exit 1
  fi
  if [ ! -w "$AGENT_LOG_DIR" ]; then
    echo "[$(timestamp)] [ERROR] log directory is not writable: $AGENT_LOG_DIR" >&2
    exit 1
  fi
  touch "$LOG_FILE" 2>/dev/null || {
    echo "[$(timestamp)] [ERROR] cannot write log file: $LOG_FILE" >&2
    exit 1
  }
  chmod g+rw "$LOG_FILE" 2>/dev/null || true
}

rotate_logs() {
  [ -f "$LOG_FILE" ] || return 0
  local size
  size="$(wc -c < "$LOG_FILE" 2>/dev/null || echo 0)"
  [ "$size" -lt "$LOG_MAX_BYTES" ] && return 0
  local i="$LOG_KEEP_COUNT"
  while [ "$i" -gt 1 ]; do
    [ -f "${LOG_FILE}.$((i - 1))" ] && mv "${LOG_FILE}.$((i - 1))" "${LOG_FILE}.${i}"
    i=$((i - 1))
  done
  mv "$LOG_FILE" "${LOG_FILE}.1"
  : > "$LOG_FILE"
}

find_pid() {
  local candidate command
  candidate="$(pgrep -x "$APP_NAME" 2>/dev/null | head -n 1 || true)"
  [ -n "$candidate" ] && printf "%s\n" "$candidate" && return 0
  pgrep -f "$APP_MATCH" | while read -r candidate; do
    [ "$candidate" = "$$" ] && continue
    command="$(ps -p "$candidate" -o args= 2>/dev/null || true)"
    case "$command" in
      *monitor.sh*|*"pgrep -f"*) continue ;;
      *) printf "%s\n" "$candidate"; return 0 ;;
    esac
  done | head -n 1
}

check_port_listen() {
  ss -tulnp 2>/dev/null | awk -v port=":${AGENT_PORT}" '$0 ~ port && $0 ~ /LISTEN/ { found=1 } END { exit found ? 0 : 1 }'
}

check_firewall() {
  if command -v ufw >/dev/null 2>&1; then
    ufw status 2>/dev/null | grep -qi "Status: active" && return 0
    grep -qi '^ENABLED=yes' /etc/ufw/ufw.conf 2>/dev/null && return 0
  fi
  if command -v firewall-cmd >/dev/null 2>&1; then
    firewall-cmd --state >/dev/null 2>&1
    return $?
  fi
  return 1
}

get_cpu_percent() {
  ps -p "$1" -o %cpu= 2>/dev/null | awk '{ printf "%.1f", $1 + 0 }'
}

get_mem_percent() {
  ps -p "$1" -o %mem= 2>/dev/null | awk '{ printf "%.1f", $1 + 0 }'
}

get_disk_percent() {
  df -P "$AGENT_HOME" 2>/dev/null | awk 'NR==2 { gsub("%", "", $5); print $5 + 0 }'
}

gt_threshold() {
  awk -v value="$1" -v threshold="$2" 'BEGIN { exit !(value > threshold) }'
}

main() {
  ensure_log_file
  rotate_logs

  local pid cpu mem disk
  pid="$(find_pid || true)"
  if [ -z "$pid" ]; then
    log_line "ERROR" "Health Check failed: process not found APP_MATCH:$APP_MATCH"
    exit 1
  fi
  if ! check_port_listen; then
    log_line "ERROR" "Health Check failed: port ${AGENT_PORT} is not LISTEN"
    exit 1
  fi
  if ! check_firewall; then
    log_line "WARNING" "firewall is not active or firewall tool is unavailable"
  fi

  cpu="$(get_cpu_percent "$pid")"
  mem="$(get_mem_percent "$pid")"
  disk="$(get_disk_percent)"

  echo "====== SYSTEM MONITOR RESULT ======"
  echo "[HEALTH CHECK]"
  echo "Checking process '${APP_NAME}'... [OK] (PID: ${pid})"
  echo "Checking port ${AGENT_PORT}... [OK]"
  echo "[RESOURCE MONITORING]"
  echo "CPU Usage : ${cpu}%"
  echo "MEM Usage : ${mem}%"
  echo "DISK Used  : ${disk}%"

  append_metric_line "$pid" "$cpu" "$mem" "$disk"
  gt_threshold "$cpu" "$CPU_WARN" && log_line "WARNING" "CPU usage exceeded threshold: CPU:${cpu}% THRESHOLD:${CPU_WARN}%"
  gt_threshold "$mem" "$MEM_WARN" && log_line "WARNING" "MEM usage exceeded threshold: MEM:${mem}% THRESHOLD:${MEM_WARN}%"
  gt_threshold "$disk" "$DISK_WARN" && log_line "WARNING" "DISK usage exceeded threshold: DISK_USED:${disk}% THRESHOLD:${DISK_WARN}%"
  echo "[INFO] Log appended: $LOG_FILE"
}

main "$@"
