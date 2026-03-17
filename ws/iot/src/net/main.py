import typer
import re
import sys
import socket
import subprocess
import ipaddress

app = typer.Typer(no_args_is_help=True)

@app.command()
def scan(netmask: str = typer.Argument(..., help="Netmask to scan (e.g., 192.168.1.0/24)")):
    """Scan the network for active IP addresses using the provided netmask."""
    print(f"Scanning network: {netmask}...")
    
    try:
        network = ipaddress.ip_network(netmask, strict=False)
    except ValueError as e:
        print(f"Error: Invalid netmask '{netmask}'. {e}")
        raise typer.Exit(code=1)

    # Simple ping sweep for the entire network
    # Note: On MacOS, -t 1 is 1 second timeout. -c 1 is 1 packet.
    # We scan all addresses in the network including network and broadcast
    # because the user might want to scan a specific IP or a very small range.
    try:
        for ip in network:
            ip_str = str(ip)
            # Using ping -c 1 -t 1 ip
            try:
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "1", ip_str],
                    capture_output=True,
                    text=True,
                    timeout=3,
                )

                # om ping är OK
                if result.returncode == 0:
                    # skriver ut IP (vit text)
                    print(ip_str)

                    # fråga efter mac-adress
                    macaddr = get_mac(ip_str)
                    
                    if macaddr:
                        # skriv ut mac addr
                        print(macaddr)

                        # kolla om det är en RPi
                        print(ispi(macaddr))
                    

                else:
                    error_msg = result.stderr.strip()
                    output = f"{ip_str} (error: {error_msg})" if error_msg else ip_str
                    typer.secho(output, fg=typer.colors.RED, err=True)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                raise
    except KeyboardInterrupt:
        print("\nScan interrupted by user. Exiting...")
        raise typer.Exit(code=0)


@app.command()
def get_mac(ip):
    try:
        # Kör 'arp -n'
        result = subprocess.check_output(["arp", "-n", ip], stderr=subprocess.STDOUT).decode()
        
        # Letar efter mönstret för en MAC-adress var som helst på raden
        match = re.search(r"([0-9a-fA-F]{1,2}(?::[0-9a-fA-F]{1,2}){5})", result)
        
        if match:
            return match.group(1)
        return None
    except Exception:
        return None

@app.command()
def ispi(mac):
    # Raspberry Pi Foundations vanligaste prefix (små bokstäver)
    # 28:CD:C1, B8:27:EB, D8:3A:DD, E4:5F:01, 3A:35:41 m.fl.
    rp_prefixes = ["28:cd:c1", "b8:27:eb", "d8:3a:dd", "e4:5f:01", "dc:a6:32", "88:a2:9e", "2c:cf:67"]

    # Rensa bort eventuella bindestreck och gör till små bokstäver
    clean_mac = mac.lower().replace("-", ":")

    # Kolla om de första 8 tecknen (XX:XX:XX) matchar listan
    if any(clean_mac.startswith(prefix) for prefix in rp_prefixes):
        return "Detta är en Raspberry Pi!\n"

    return "Ingen raspberry Pi\n"


@app.command()
def other():
    """Dummy command to avoid command name being collapsed."""
    pass

if __name__ == "__main__":
    app()
