# 제출 증거 체크리스트

- [ ] SSH 포트 20022 확인: `ss -tulnp | grep 20022`
- [ ] Root 원격 차단 설정: `grep PermitRootLogin /etc/ssh/sshd_config`
- [ ] 방화벽 20022/15034 only: `sudo ufw status numbered`
- [ ] 계정/그룹 확인: `id agent-admin`, `id agent-dev`, `id agent-test`
- [ ] 디렉터리 권한 확인: `ls -ld /opt/agent-app/* /var/log/agent-app`
- [ ] 환경변수 확인: `env | grep AGENT_`
- [ ] Boot Sequence 5단계 OK 및 `Agent READY`
- [ ] 15034 LISTEN: `ss -tulnp | grep 15034`
- [ ] monitor.sh 실행 결과
- [ ] `/var/log/agent-app/monitor.log` 누적
- [ ] agent-admin crontab 매분 실행
