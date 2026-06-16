# 문제 3: evollard 인증과 유료 리포트 인가

로그인한 고객만 리포트를 조회하고, 운영자만 `paid_report_issued` 상태로 변경합니다.

## 실행

```bash
pip install fastapi uvicorn python-multipart itsdangerous
uvicorn main:app --reload
```

## 테스트 계정

| 계정 | 비밀번호 | 역할 |
|---|---|---|
| collector | demo123 | 고객 |
| operator | demo123 | 운영자 |

## 공개/보호 경로

| 경로 | 접근 |
|---|---|
| `/`, `/login` | 공개 |
| `/reports` | 로그인 필요 |
| `/operator`, `/reports/{id}/issue` | 운영자 권한 필요 |
