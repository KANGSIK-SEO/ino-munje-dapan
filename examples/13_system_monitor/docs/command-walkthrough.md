# Linux/Shell 명령어 해설

문제 13은 단순 문서가 아니라 실제 운영자가 서버를 준비하고 관제하는 흐름으로 풀었다.

## 1. 계정과 그룹

```bash
sudo groupadd agent-common
sudo groupadd agent-core
sudo useradd -m -s /bin/bash -G agent-common,agent-core agent-admin
sudo useradd -m -s /bin/bash -G agent-common,agent-core agent-dev
sudo useradd -m -s /bin/bash -G agent-common agent-test
id agent-admin
id agent-dev
id agent-test
```

- `agent-common`: 업로드 파일 접근 그룹
- `agent-core`: API Key와 로그 접근 그룹
- `agent-admin`: cron 등록과 운영 확인 담당
- `agent-dev`: 앱과 관제 스크립트 소유자
- `agent-test`: 업로드 영역만 접근 가능한 테스트 사용자

## 2. 디렉터리와 권한

```bash
sudo mkdir -p /opt/agent-app/{upload_files,api_keys,bin}
sudo mkdir -p /var/log/agent-app
sudo chown -R agent-dev:agent-common /opt/agent-app
sudo chown -R agent-dev:agent-core /opt/agent-app/api_keys /opt/agent-app/bin /var/log/agent-app
sudo chmod 770 /opt/agent-app/upload_files
sudo chmod 770 /opt/agent-app/api_keys /var/log/agent-app
ls -ld /opt/agent-app /opt/agent-app/upload_files /opt/agent-app/api_keys /var/log/agent-app
```

권한을 분리한 이유는 업로드 파일과 API Key/로그의 민감도가 다르기 때문이다. 테스트 사용자는 업로드 파일에는 접근할 수 있지만 API Key에는 접근하지 못해야 한다.

## 3. SSH와 방화벽

```bash
sudo sed -i 's/^#Port 22/Port 20022/' /etc/ssh/sshd_config
sudo sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
ss -tulnp | grep 20022

sudo ufw default deny incoming
sudo ufw allow 20022/tcp
sudo ufw allow 15034/tcp
sudo ufw enable
sudo ufw status numbered
```

- SSH 기본 포트 22를 20022로 바꿔 무차별 대입 시도를 줄인다.
- Root 원격 로그인을 막아 계정 탈취 위험을 낮춘다.
- 방화벽은 SSH 20022와 Agent API 15034만 연다.

## 4. 앱 실행 환경

```bash
export AGENT_HOME=/opt/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=/opt/agent-app/upload_files
export AGENT_KEY_PATH=/opt/agent-app/api_keys/t_secret.key
export AGENT_LOG_DIR=/var/log/agent-app
echo agent_api_key_test | sudo tee /opt/agent-app/api_keys/t_secret.key
ss -tulnp | grep 15034
```

환경변수로 경로와 포트를 고정하면 서버가 바뀌어도 실행 조건을 재현하기 쉽다.

## 5. 관제 스크립트 내부 명령

`bin/monitor.sh`는 다음 명령을 사용한다.

```bash
pgrep -x "$APP_NAME"
pgrep -f "$APP_MATCH"
ps -p "$pid" -o %cpu=
ps -p "$pid" -o %mem=
ss -tulnp
df -P "$AGENT_HOME"
awk
wc -c
mv
touch
chmod
```

- `pgrep`, `ps`: 프로세스 존재와 CPU/MEM 사용률 확인
- `ss`: 15034 포트 LISTEN 확인
- `df`: 디스크 사용률 확인
- `awk`: 숫자 포맷팅과 임계값 비교
- `wc`, `mv`: 로그 크기 확인과 회전

## 6. cron 등록

```bash
sudo -u agent-admin crontab -e
```

등록 내용:

```cron
* * * * * AGENT_HOME=/opt/agent-app AGENT_PORT=15034 AGENT_LOG_DIR=/var/log/agent-app /opt/agent-app/bin/monitor.sh >/dev/null 2>&1
```

매분 관제 결과가 `/var/log/agent-app/monitor.log`에 누적된다.

## 7. 제출 증거

```bash
tail -n 20 /var/log/agent-app/monitor.log
crontab -l
sudo ufw status numbered
ss -tulnp | grep -E '20022|15034'
ps -ef | grep agent
```

위 명령 결과를 캡처하면 SSH, 방화벽, 프로세스, 포트, cron, 로그 누적 증거를 한 번에 제시할 수 있다.
