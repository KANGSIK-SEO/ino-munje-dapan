# evollard Git 협업 시나리오

문제 10은 3인 팀이 `evollard` 유료 리포트 서비스를 GitHub Flow로 개발한다고 가정해 풀었다.

## 팀 역할

| 사용자 | 담당 |
|---|---|
| User A | 감정 요청 CRUD |
| User B | 유료 리포트 발행 화면 |
| User C | Linux 관제/장애 문서 |

## 브랜치 전략

```text
main
  feature/request-crud
  feature/paid-report
  feature/linux-monitor
  docs/troubleshooting-log
```

`main`은 배포 가능한 상태로 유지하고, 모든 변경은 PR로 병합한다.

## 이슈 기반 작업

```bash
gh issue create --title "감정 요청 CRUD 구현" --body "작품 감정 신청 등록/조회/수정/삭제"
gh issue create --title "유료 리포트 발행 상태 추가" --body "reviewed 상태를 paid_report_issued로 변경"
gh issue create --title "Agent 관제 스크립트 작성" --body "프로세스/포트/CPU/MEM/DISK 로그 수집"
```

## User A 작업

```bash
git checkout main
git pull origin main
git checkout -b feature/request-crud
git add examples/04_fastapi_crud
git commit -m "feat: add authentication request crud"
git push origin feature/request-crud
gh pr create --title "감정 요청 CRUD 구현" --body "What: CRUD 추가
Why: 고객 감정 신청 관리
How to test: uvicorn main:app --reload"
```

## User B 작업

```bash
git checkout main
git pull origin main
git checkout -b feature/paid-report
git add examples/03_fastapi_auth
git commit -m "feat: add protected paid reports"
git push origin feature/paid-report
gh pr create --title "유료 리포트 보호 화면 추가" --body "What: 로그인/권한/발행 상태 추가
Why: 유료 리포트는 고객과 운영자 권한이 필요
How to test: collector/operator 계정 로그인"
```

## User C 작업

```bash
git checkout main
git pull origin main
git checkout -b feature/linux-monitor
git add examples/13_system_monitor examples/12_linux_troubleshooting
git commit -m "feat: add linux monitor and incident reports"
git push origin feature/linux-monitor
gh pr create --title "Linux 관제와 장애 리포트 추가" --body "What: monitor.sh와 장애 이슈 문서
Why: 분석 Agent 운영 증거 필요
How to test: bash bin/monitor.sh"
```

## 리뷰 예시

```text
review: status 값은 submitted/analyzing/reviewed/paid_report_issued/rejected 중 하나로 제한하는 것이 좋겠습니다.
reply: SQL CHECK 제약과 FastAPI select option에 같은 상태 값을 맞췄습니다.
```

```text
review: monitor.sh가 자기 자신을 pgrep 결과로 잡을 수 있습니다.
reply: command 문자열에서 monitor.sh와 pgrep -f를 제외하도록 필터를 추가했습니다.
```

## 병합 후 확인

```bash
git checkout main
git pull origin main
git log --oneline --graph --all --decorate -n 20
```

예상 히스토리:

```text
* merge PR #3 feat: add linux monitor and incident reports
* merge PR #2 feat: add protected paid reports
* merge PR #1 feat: add authentication request crud
* initial evollard mission repository
```
