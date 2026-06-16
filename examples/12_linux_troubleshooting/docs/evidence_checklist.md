# 증거 체크리스트

## OOM

- [ ] `monitor.sh` 메모리 상승 로그
- [ ] 종료 직전 `MemoryGuard` 로그
- [ ] 종료 직후 Health Check 실패 로그
- [ ] `MEMORY_LIMIT` 변경 전후 비교

## CPU Spike

- [ ] `top` 또는 `ps` CPU 캡처
- [ ] `WATCHDOG SIGTERM` 로그
- [ ] `CPU_MAX_OCCUPY` 변경 전후 비교

## Deadlock

- [ ] `ps -ef` PID 존재 증거
- [ ] `top -H` 또는 `ps -L` 스레드 증거
- [ ] 마지막 `WAITING/BLOCKED` 로그
- [ ] `MULTI_THREAD_ENABLE` 변경 전후 비교
