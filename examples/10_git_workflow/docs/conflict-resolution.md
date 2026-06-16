# Conflict Resolution Log

## Case 1. 리포트 상태명 충돌

- Symptom: `examples/03_fastapi_auth/main.py`에서 User A는 `issued`, User B는 `paid_report_issued` 상태명을 사용했다.
- File: `examples/03_fastapi_auth/main.py`, `examples/05_sql_database/schema.sql`
- Cause: 백엔드 코드와 SQL CHECK 제약의 상태 enum이 달랐다.
- Command:

```bash
git status
git pull origin main
git diff
```

- Decision: SQL과 FastAPI 모두 `paid_report_issued`로 통일했다.
- Result: 리포트 발행 상태가 DB/화면/문서에서 같은 이름으로 표현된다.

## Case 2. monitor.sh 프로세스 탐지 충돌

- Symptom: `pgrep -f agent`가 실제 Agent가 아니라 `monitor.sh` 자신을 잡는 문제가 생겼다.
- File: `examples/13_system_monitor/bin/monitor.sh`
- Cause: User C는 단순 `pgrep -f`, 리뷰어는 자기 자신 제외 로직을 추가했다.
- Command:

```bash
git status
git diff examples/13_system_monitor/bin/monitor.sh
ps -ef | grep agent
```

- Decision: `monitor.sh`와 `pgrep -f`가 들어간 command는 제외하고 첫 번째 실제 Agent PID만 선택한다.
- Result: 관제 스크립트가 자기 자신을 정상 프로세스로 오인하지 않는다.

## Conflict Marker Meaning

```text
[current branch]
현재 브랜치 내용
[incoming branch]
병합하려는 브랜치 내용
[end conflict]
```

충돌 마커를 그대로 커밋하면 안 된다. 두 변경의 의도를 비교한 뒤 최종 문장/코드만 남긴다.
