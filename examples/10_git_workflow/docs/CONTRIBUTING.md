# evollard Contributing Guide

## Branch Rule

- `main`은 항상 제출 가능한 상태로 유지한다.
- 기능은 `feature/<topic>` 브랜치에서 작업한다.
- 문서는 `docs/<topic>` 브랜치도 허용한다.
- 병합은 Pull Request로만 한다.

## Branch Examples

```text
feature/request-crud
feature/paid-report
feature/linux-monitor
docs/incident-report
```

## Commit Rule

```text
feat: 새로운 기능
fix: 버그 수정
docs: 문서 수정
refactor: 구조 개선
test: 테스트 추가
chore: 설정/정리
```

좋은 예:

```bash
git commit -m "feat: add protected paid reports"
git commit -m "docs: add linux incident report checklist"
```

나쁜 예:

```bash
git commit -m "update"
git commit -m "fix"
```

## Pull Request Rule

PR 본문은 반드시 아래 세 섹션을 포함한다.

```md
## What
- 무엇을 바꿨는가

## Why
- 왜 필요한가

## How to Test
- 어떻게 확인하는가
```

## Review Rule

- 본인 PR은 본인이 승인하지 않는다.
- 리뷰는 최소 1개 이상의 구체적인 코멘트를 남긴다.
- 단순 오탈자보다 상태 전이, 권한, 보안, 실행 방법을 우선 검토한다.

## Conflict Rule

충돌이 나면 다음 순서로 해결한다.

```bash
git status
git pull origin main
# conflict 파일 수정
git add <file>
git commit
git push
```

충돌 원인과 결정은 `conflict-resolution.md`에 기록한다.
