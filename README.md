# evollard Mission Repository

`문제.txt`의 13개 미션을 하나의 가짜 미술품 판별 서비스 `evollard`를 완성하는 과정으로 재구성한 단일 Git 저장소입니다.

`evollard`는 작품 이미지와 작품 정보를 받아 위작 위험도를 분석하고, 근거가 포함된 유료 감정 리포트를 발행하는 서비스입니다. 각 문제는 독립 과제가 아니라 `evollard`라는 그릇을 만들기 위한 재료입니다.

## 최종 서비스 그림

1. 고객이 작품 감정을 신청한다.
2. 작품, 작가, 소장 이력, 분석 로그가 데이터베이스에 저장된다.
3. FastAPI 백엔드가 감정 요청, 리포트 조회, 상태 변경을 처리한다.
4. React SPA와 포트폴리오 페이지가 고객/운영자 화면을 제공한다.
5. AWS 인프라에 배포하고 Linux 관제로 운영 증거를 남긴다.
6. 장애는 GitHub Issue 형태로 기록한다.
7. Mini Git/Mini Redis 구현으로 버전 기록과 캐시 원리를 학습한다.
8. 팀 협업과 AI 커밋/PR 생성기로 개발 흐름을 자동화한다.

## 문제 재구성 순서

| 순서 | 원문 문제 | evollard에서의 의미 | 산출물 |
|---:|---:|---|---|
| 1 | 11 | 감정 수익/비용/리포트 매출을 기록하는 파일 기반 운영 장부 | `examples/11_budget_app` |
| 2 | 5 | 작가, 작품, 감정 요청, 유료 리포트 관계형 DB 설계 | `examples/05_sql_database` |
| 3 | 4 | 감정 요청 CRUD 웹 백엔드 | `examples/04_fastapi_crud` |
| 4 | 3 | 로그인, 고객/리포트/상태 변경이 있는 보호 서비스 | `examples/03_fastapi_auth` |
| 5 | 6 | 감정 현황, 작품 상세, 리포트 발행 SPA | `examples/06_react_spa` |
| 6 | 7 | evollard 공개 포트폴리오/랜딩 사이트 | `examples/07_portfolio` |
| 7 | 2 | 유료 리포트 서비스 배포용 AWS 인프라 | `examples/02_aws_infra` |
| 8 | 13 | 분석 Agent와 리포트 서버 관제 자동화 | `examples/13_system_monitor` |
| 9 | 12 | OOM/CPU/Deadlock 장애 이슈 리포트 | `examples/12_linux_troubleshooting` |
| 10 | 8 | 감정 리포트 변경 이력을 이해하기 위한 Mini Git | `examples/08_mini_git` |
| 11 | 9 | 분석 결과 캐시/TTL 원리를 이해하기 위한 Mini Redis | `examples/09_mini_redis` |
| 12 | 10 | 팀 단위 리포트 서비스 개발 워크플로우 | `examples/10_git_workflow` |
| 13 | 1 | 감정 모델/리포트 코드 변경사항 AI 커밋/PR 자동화 | `examples/01_ai_gitgen` |

## 읽는 문서

- [제출 설명서](./SUBMISSION.md)
- [evollard 문제 연결 지도](./docs/evollard-problem-map.md)
- [스토리 기반 로드맵](./docs/story-roadmap.md)
- [유료 감정 리포트 샘플](./docs/paid-report-sample.md)
- [기존 1~10번 프로그램 설계](./10개_문제_프로그램_설계.md)

## 빠른 실행 예

```bash
cd examples/11_budget_app
python -m budget_app category add 리포트매출
python -m budget_app category add 분석비용
python -m budget_app add --type income --date 2026-06-16 --amount 49000 --category 리포트매출 --memo "유료 감정 리포트 EVR-0001 발행" --tags report,paid
python -m budget_app summary --month 2026-06
```

```bash
cd examples/05_sql_database
sqlite3 evollard.db < schema.sql
sqlite3 evollard.db < seed.sql
sqlite3 evollard.db < queries.sql
```

## 제출 기준

하나의 GitHub 저장소에 전체를 push합니다. README는 문제 번호가 아니라 `evollard` 완성 흐름으로 설명하고, 각 문제 산출물은 `examples/` 아래에서 확인할 수 있게 둡니다.

민감정보, 결제 키, AI API Key, AWS Access Key, SSH private key는 커밋하지 않습니다.
