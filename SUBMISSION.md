# evollard 제출 설명서

## 내가 푼 문제의 큰 그림

이 저장소는 13개 문제를 따로 푼 답안집이 아니라, `evollard`라는 가짜 미술품 검증 서비스를 완성하는 하나의 제품형 풀이입니다.

`evollard`의 최종 결과물은 고객이 작품 감정을 신청하면 분석 결과와 근거를 정리한 유료 리포트를 발행하는 서비스입니다. 각 문제는 이 서비스를 만들기 위한 재료로 배치했습니다.

## 문제별 풀이 설명

| 문제 | 풀이 위치 | 내가 만든 것 | evollard에서의 역할 |
|---:|---|---|---|
| 1 | `examples/01_ai_gitgen` | Git diff 기반 커밋/PR 생성 CLI | 분석 엔진 변경사항을 PR 문서로 자동 정리 |
| 2 | `examples/02_aws_infra` | VPC/EC2/Security Group CloudFormation | 유료 리포트 서버 배포 인프라 |
| 3 | `examples/03_fastapi_auth` | 로그인/인가/리포트 발행 상태 변경 | 고객은 리포트 조회, 운영자는 발행 처리 |
| 4 | `examples/04_fastapi_crud` | 감정 요청 CRUD 웹 | 작품 감정 신청 등록/조회/수정/삭제 |
| 5 | `examples/05_sql_database` | 작가/작품/감정요청/유료리포트 SQL | 서비스 핵심 데이터 모델 |
| 6 | `examples/06_react_spa` | React SPA 예시 | 운영자 대시보드의 출발점 |
| 7 | `examples/07_portfolio` | 순수 HTML/CSS/JS 포트폴리오 | evollard 소개/사례 공개 페이지 |
| 8 | `examples/08_mini_git` | Mini Git CLI | 리포트 버전 이력 원리 학습 |
| 9 | `examples/09_mini_redis` | Mini Redis CLI | 분석 결과 캐시/TTL/LRU 원리 학습 |
| 10 | `examples/10_git_workflow` | Git 협업 문서/명령 시나리오 | 팀 개발과 PR 리뷰 증빙 |
| 11 | `examples/11_budget_app` | 파일 기반 운영 장부 CLI | 유료 리포트 매출/분석비용 기록 |
| 12 | `examples/12_linux_troubleshooting` | OOM/CPU/Deadlock 이슈 리포트 | 분석 Agent 장애 대응 문서 |
| 13 | `examples/13_system_monitor` | Bash 관제 스크립트와 Linux 설정 명령 | 서버 리소스/포트/로그 관제 |

## 리눅스와 쉘 명령어를 어디에 썼나

문제 13은 `examples/13_system_monitor`에 풀었습니다.

- `bin/monitor.sh`: Bash로 작성한 실제 관제 스크립트
- `docs/setup_commands.md`: 사용자/그룹/권한/SSH/UFW/cron 설정 명령
- `docs/command-walkthrough.md`: 사용한 쉘 명령어와 의미 설명
- `docs/evidence_checklist.md`: 제출 증거 체크리스트

핵심 쉘 명령은 다음 범주로 나눴습니다.

- 계정/그룹: `groupadd`, `useradd`, `id`
- 권한: `chown`, `chmod`, `ls -ld`
- 네트워크/보안: `ss`, `ufw`, `systemctl`
- 프로세스 관제: `pgrep`, `ps`
- 리소스 관제: `df`, `awk`, `wc`
- 로그/스케줄: `touch`, `crontab`, 로그 회전용 `mv`

## Git 협업 내용은 어디에 있나

문제 10은 `examples/10_git_workflow`에 풀었습니다.

- `docs/CONTRIBUTING.md`: 브랜치, 커밋, PR, 리뷰 규칙
- `docs/collaboration-scenario.md`: 3인 팀 협업 시나리오와 실제 Git 명령
- `docs/conflict-resolution.md`: 충돌 2건 해결 기록
- `docs/troubleshooting-log.md`: amend/reset/revert/stash 명령 기록

협업 흐름은 `main`을 보호하고 `feature/*` 브랜치에서 작업한 뒤 PR로 병합하는 GitHub Flow입니다.

## 실행 검증

### 파일 기반 운영 장부

```bash
cd examples/11_budget_app
python3 -m budget_app category add 리포트매출
python3 -m budget_app category add 분석비용
python3 -m budget_app add --type income --date 2026-06-16 --amount 49000 --category 리포트매출 --memo "유료 감정 리포트 EVR-0001 발행" --tags report,paid
python3 -m budget_app add --type expense --date 2026-06-16 --amount 12000 --category 분석비용 --memo "이미지 분석 Agent 실행 비용" --tags ai,cost
python3 -m budget_app summary --month 2026-06
```

예상 결과:

```text
income=49000
expense=12000
balance=37000
category_top
- 분석비용: 12000
```

### SQL 데이터베이스

```bash
cd examples/05_sql_database
sqlite3 evollard.db < schema.sql
sqlite3 evollard.db < seed.sql
sqlite3 evollard.db < queries.sql
```

`paid_report` 매출 합계, 상태별 감정 요청 수, 위험도 평균 이상 요청 등을 확인합니다.

### FastAPI 감정 요청/리포트

```bash
cd examples/04_fastapi_crud
uvicorn main:app --reload
```

```bash
cd examples/03_fastapi_auth
uvicorn main:app --reload
```

테스트 계정:

- `collector / demo123`: 고객 리포트 조회
- `operator / demo123`: 유료 리포트 발행 상태 변경

## 최종적으로 보여주려는 실력

이 풀이는 단순히 “문제를 하나씩 맞췄다”가 아니라, 데이터베이스, 백엔드, 프론트엔드, 클라우드, 리눅스 운영, 장애 분석, Git 협업, AI 자동화를 모두 하나의 서비스 맥락으로 묶었습니다.

채점자는 이 저장소를 보면서 `evollard`가 어떻게 유료 리포트를 발행하는 서비스로 완성되는지 따라갈 수 있습니다.
