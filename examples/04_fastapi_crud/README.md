# 문제 4: evollard 감정 요청 CRUD

작품 감정 신청을 등록, 목록 조회, 상세 조회, 수정, 삭제하는 FastAPI SSR 예시입니다.

## 실행

```bash
pip install fastapi uvicorn python-multipart
uvicorn main:app --reload
```

## 구현 포인트

- 홈/목록/상세/등록/수정 화면
- HTML Form + `Form()`
- POST 후 `RedirectResponse(..., status_code=303)`
- Router 함수, Service, Repository 역할 분리
- 위험도 0~100 검증
