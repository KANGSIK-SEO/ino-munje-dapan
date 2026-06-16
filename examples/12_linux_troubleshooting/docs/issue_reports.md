# 장애 이슈 리포트 3건

## Issue 1. OOM / Memory Leak

### Description
- 현상: 실행 후 시간이 지날수록 RSS 메모리가 증가하고 `MemoryGuard`가 프로세스를 종료했다.
- 재현 조건: `MEMORY_LIMIT=64`로 낮게 설정한 뒤 업로드/처리 요청을 반복했다.
- 영향: 15034 포트의 Agent API가 일시 중단되어 Health Check가 실패했다.

### Evidence & Logs
- `monitor.sh`: `MEM:8.2% -> 10.5% -> 13.1%`로 지속 상승
- 종료 직전 로그: `MemoryGuard limit exceeded`
- 종료 직후 로그: `Health Check failed: process not found`
- 비교: `MEMORY_LIMIT=64`에서는 종료, `MEMORY_LIMIT=256`에서는 동일 요청 5분간 정상

### Root Cause Analysis
- 요청 처리 중 생성된 버퍼 또는 캐시가 해제되지 않는 패턴으로 추정된다.
- 메모리 사용량 증가가 요청 횟수와 함께 누적되었고, 유휴 상태에서도 감소하지 않았다.

### Workaround & Verification
- 조치: 제한값을 임시 상향하고, 요청 처리 후 임시 파일/버퍼 정리 루틴을 점검 대상으로 등록했다.
- 검증: 제한값 상향 후 Health Check가 유지되고 monitor.log가 누적되었다.
- 재발 방지: RSS 추세 경고와 업로드 크기 제한을 추가한다.

## Issue 2. CPU Spike

### Description
- 현상: 특정 PID가 CPU를 장시간 점유하고 Watchdog가 종료했다.
- 재현 조건: `CPU_MAX_OCCUPY=20`에서 계산 부하 요청을 반복했다.
- 영향: 응답 지연과 Health Check 불안정이 발생했다.

### Evidence & Logs
- `top`: 대상 PID CPU 사용률이 80% 이상 유지
- `ps -p <PID> -o %cpu,%mem,args`: CPU 과점유 확인
- 로그: `WATCHDOG SIGTERM CPU limit exceeded`
- 비교: `CPU_MAX_OCCUPY=20` 종료, `CPU_MAX_OCCUPY=80` 지연은 있으나 종료 없음

### Root Cause Analysis
- CPU bound 작업이 요청 스레드 안에서 동기 실행되었다.
- 제한값 초과 시 Watchdog가 전체 프로세스를 보호하기 위해 SIGTERM을 보냈다.

### Workaround & Verification
- 조치: CPU 제한값을 서비스 특성에 맞게 재설정하고, 무거운 작업은 큐/워커 분리를 권고했다.
- 검증: 조정 후 5분 동안 API 포트와 PID가 유지되었다.
- 재발 방지: CPU 임계값 경고와 요청별 timeout을 둔다.

## Issue 3. Deadlock

### Description
- 현상: 프로세스는 살아 있고 포트도 열려 있지만 요청 처리가 멈췄다.
- 재현 조건: `MULTI_THREAD_ENABLE=true`에서 동시 요청을 반복했다.
- 영향: 장애 탐지 전까지 API 응답이 무기한 대기했다.

### Evidence & Logs
- `ps -ef`: PID 존재
- `top -H` 또는 `ps -L`: 여러 스레드가 낮은 CPU로 장시간 유지
- 마지막 로그: `WAITING resource=A`, `BLOCKED resource=B`
- 비교: `MULTI_THREAD_ENABLE=false`에서는 같은 요청이 순차 처리되어 멈춤 없음

### Root Cause Analysis
- Deadlock 4대 조건이 동시에 충족된 것으로 판단했다.
- 상호 배제: 락 자원 A/B는 한 스레드만 소유
- 점유 대기: A를 가진 스레드가 B를 기다림
- 비선점: 다른 스레드의 락을 강제로 빼앗지 못함
- 순환 대기: A -> B, B -> A 대기 고리

### Workaround & Verification
- 조치: 락 획득 순서를 고정하고 임시로 멀티스레드를 비활성화했다.
- 검증: 동일 요청 반복 시 WAITING/BLOCKED 로그가 재현되지 않았다.
- 재발 방지: 락 순서 문서화, timeout, 동시성 테스트를 추가한다.
