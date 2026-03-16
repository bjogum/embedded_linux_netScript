# edu-embedded-linux

## Reset fingerprint (if needed)

```
ssh-keygen -R "[localhost]:2225"
```

## Connect

```bash
cd ~
cd ws
git clone https://github.com/miwashi-edu/edu-embedded-linux.git
cd edu-embedded-linux
git switch level-5
./start-iotnet.sh # If not started already
docker compose down
docker compose up -d --build
ssh -p 2225 dev@localhost #password dev
```
## Prepare (only once)

> Create an `empty` repository in github, it must be empty.
> Copy the `URL` to this repository
> Remember you need to create a `Persona Access Token` as password.

### Prepare GIT

```bash
git config --global init.defaultBranch main
git config --global user.name "you name"
git config --global user.email "user@example.com"
cd ~
cd ws
cd iot
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/miwashi-edu/iot.git
git push -u origin main
```

### Prepare Rest

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
sudo apt update
sudo apt install curl
sudo apt install iputils-ping 
sudo apt install net-tools
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Instructions

```bash
cd ~
cd ws
cd iot
uv run iot scan 192.168.1.0/27 2>/dev/null
```

## Instructions

```bash
pip install . --break-system-packages
hello
iot scan 192.168.1.0/27 2>/dev/null
```

## Start over

```bash
git reset --hard
git clean -df
```
