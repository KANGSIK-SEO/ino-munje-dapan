# 문제 12: 리눅스 프로세스 및 시스템 리소스 트러블슈팅

운영 중인 `evollard` 분석 Agent에서 OOM, CPU Spike, Deadlock이 발생했다고 가정하고 GitHub Issue 형태로 기록합니다.

## 제출 파일

- `docs/issue_reports.md`: 장애 3종 이슈 리포트
- `docs/evidence_checklist.md`: 캡처/로그 증거 체크리스트

## 실습 기준

- 앱은 일반 사용자로 실행
- `AGENT_PORT=15034`
- `MEMORY_LIMIT`, `CPU_MAX_OCCUPY`, `MULTI_THREAD_ENABLE` 값을 바꾸며 Before/After 비교
- `monitor.sh`, `ps`, `top`, `top -H`, `ps -L`, 로그 파일을 증거로 사용
