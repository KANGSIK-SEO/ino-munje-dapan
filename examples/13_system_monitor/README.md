# 문제 13: 시스템 관제 자동화 스크립트

`evollard` 분석 Agent 운영 서버의 계정/권한/방화벽/관제 로그를 자동화하는 제출 패키지입니다.

## 파일

- `bin/monitor.sh`: 프로세스, 포트, 방화벽, CPU/MEM/DISK, 로그 회전 점검
- `docs/setup_commands.md`: Ubuntu 22.04 기준 설정 명령
- `docs/evidence_checklist.md`: 제출 증거 체크리스트

## 실행 예

```bash
AGENT_HOME=/opt/agent-app \
AGENT_PORT=15034 \
AGENT_LOG_DIR=/var/log/agent-app \
bin/monitor.sh
```
