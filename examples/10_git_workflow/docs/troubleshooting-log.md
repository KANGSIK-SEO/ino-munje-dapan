# Git Troubleshooting Log

## 1. commit --amend

- Situation: PR 본문에는 유료 리포트 발행 기능을 적었지만 커밋 메시지가 `feat: update auth`로 모호했다.
- Command:

```bash
git commit --amend -m "feat: add protected paid reports"
git push --force-with-lease origin feature/paid-report
```

- Result: 커밋 메시지가 기능을 정확히 설명하게 됐다.
- Note: 이미 공유된 브랜치에서는 팀원에게 알리고 `--force-with-lease`만 사용한다.

## 2. reset --soft

- Situation: SQL 스키마와 seed를 따로 커밋해야 하는데 실수로 README 수정까지 한 커밋에 들어갔다.
- Command:

```bash
git reset --soft HEAD~1
git status
git add examples/05_sql_database
git commit -m "feat: add evollard sql schema"
git add README.md
git commit -m "docs: explain evollard mission story"
```

- Result: 커밋 단위가 DB 구현과 문서 설명으로 나뉘었다.

## 3. revert

- Situation: 리포트 가격 계산을 잘못 바꾼 커밋이 이미 main에 병합됐다.
- Command:

```bash
git log --oneline
git revert <bad_commit_hash>
git push origin main
```

- Result: 히스토리를 지우지 않고 잘못된 변경만 되돌렸다.

## 4. stash / stash pop

- Situation: `monitor.sh`를 수정하던 중 main의 최신 변경을 먼저 받아야 했다.
- Command:

```bash
git status
git stash push -m "wip monitor threshold tuning"
git pull origin main
git stash pop
```

- Result: 작업 중인 변경을 임시 보관한 뒤 최신 main 위에 다시 적용했다.

## 5. log graph evidence

협업 증빙용 히스토리는 다음 명령으로 캡처한다.

```bash
git log --oneline --graph --all --decorate -n 30
```
