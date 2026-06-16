# Ubuntu 22.04 설정 명령

```bash
sudo groupadd agent-common
sudo groupadd agent-core
sudo useradd -m -s /bin/bash -G agent-common,agent-core agent-admin
sudo useradd -m -s /bin/bash -G agent-common,agent-core agent-dev
sudo useradd -m -s /bin/bash -G agent-common agent-test

sudo mkdir -p /opt/agent-app/{upload_files,api_keys,bin}
sudo mkdir -p /var/log/agent-app
sudo chown -R agent-dev:agent-common /opt/agent-app
sudo chown -R agent-dev:agent-core /opt/agent-app/api_keys /opt/agent-app/bin /var/log/agent-app
sudo chmod 770 /opt/agent-app/upload_files
sudo chmod 770 /opt/agent-app/api_keys /var/log/agent-app

echo agent_api_key_test | sudo tee /opt/agent-app/api_keys/t_secret.key
sudo chown agent-dev:agent-core /opt/agent-app/api_keys/t_secret.key
sudo chmod 660 /opt/agent-app/api_keys/t_secret.key
```

```bash
sudo sed -i 's/^#Port 22/Port 20022/' /etc/ssh/sshd_config
sudo sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

sudo ufw default deny incoming
sudo ufw allow 20022/tcp
sudo ufw allow 15034/tcp
sudo ufw enable
```

```bash
sudo -u agent-admin crontab -e
# Add:
* * * * * AGENT_HOME=/opt/agent-app AGENT_PORT=15034 AGENT_LOG_DIR=/var/log/agent-app /opt/agent-app/bin/monitor.sh >/dev/null 2>&1
```
