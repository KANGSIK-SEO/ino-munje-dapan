# 문제 11: evollard 운영 장부 콘솔 프로그램

`evollard`의 유료 리포트 매출, 분석 비용, 클라우드 비용, 환불 내역을 파일에 저장하고 검색/요약/예산/카테고리/import/export를 처리합니다.

## 실행

```bash
python -m budget_app --help
python -m budget_app category add 리포트매출
python -m budget_app category add 분석비용
python -m budget_app budget set --month 2026-06 --amount 500000
python -m budget_app add --type income --date 2026-06-16 --amount 49000 --category 리포트매출 --memo "유료 감정 리포트 EVR-0001 발행" --tags report,paid
python -m budget_app add --type expense --date 2026-06-16 --amount 12000 --category 분석비용 --memo "이미지 분석 Agent 실행 비용" --tags ai,cost
python -m budget_app list --limit 5
python -m budget_app search --month 2026-06 --category 리포트매출
python -m budget_app summary --month 2026-06 --top 3
python -m budget_app export --out data/june.csv --month 2026-06
```

## 저장 파일

- `data/transactions.jsonl`
- `data/categories.json`
- `data/budgets.json`

## 구현 포인트

- 표준 라이브러리만 사용
- `dataclass` 모델
- Repository/Service/CLI 분리
- `yield` 기반 최신순 스트리밍
- 데코레이터로 CLI 예외 처리
- 임시 파일 후 `os.replace`로 안전한 재작성
