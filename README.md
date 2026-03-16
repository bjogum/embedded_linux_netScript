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
./start-iotnet.sh # If not started already
docker compose down
docker compose up -d --build
ssh -p 2225 dev@localhost #password dev
```
## Prepare (only once)

```bash
```

## Instructions

```bash
```

## Instructions

```bash
pip install . --break-system-packages
hello
```

## Start over

```bash
git reset --hard
git clean -df
```
