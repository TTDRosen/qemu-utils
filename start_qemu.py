import argparse
import json
from pathlib import Path
import psutil
import subprocess
import signal
import sys

def get_network_interfaces():
    interfaces = psutil.net_if_addrs().keys()
    return interfaces

if_pattern = "enp"

def setup_bridge():
    subprocess.run(["brctl", "addbr", "br0"], check=True)

    interfaces = list(filter(lambda x: x.startswith(if_pattern), get_network_interfaces()))
    assert len(interfaces) == 1, interfaces

    subprocess.run(["brctl", "addif", "br0", interfaces[0]], check=True)
    subprocess.run(["dhclient", "br0"], check=True)

def teardown_bridge(allow_failure=False):
    subprocess.run(["ip", "link", "set", "br0", "down"], check=not allow_failure)

    interfaces = list(filter(lambda x: x.startswith(if_pattern), get_network_interfaces()))
    assert len(interfaces) == 1, interfaces

    subprocess.run(["brctl", "delif", "br0", interfaces[0]], check=not allow_failure)
    subprocess.run(["brctl", "delbr", "br0"], check=not allow_failure)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cpu")

    args = parser.parse_args()

    instructions = json.load(open(f"images/{args.cpu}/cmd.json"))

    files = instructions["files"]

    for file, cmds in files.items():
        path = Path(file)
        if not path.exists():
            print(f"{path} doesn't exist now downloading")
            path.parent.mkdir(parents=True, exist_ok=True)
            for cmd in cmds:
                print(f"\t>>> {cmd}")
                subprocess.run(cmd, cwd=Path(__file__).parent, check=True, shell=True)
            assert path.exists(), f"After running commands to generate {path}, it still didn't exist"

    # teardown_bridge(allow_failure = True)
    # setup_bridge()

    cmd = instructions["cmd"]

    output = subprocess.run(["lspci", "-n", "-D", "-d", "1e52:"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
    for device in output.stdout.splitlines():
        device = device.decode().strip()
        id = device.split()[0]

        cmd.extend(["-device", f"vfio-pci,host={id}"])

    # Add sudo to allow for forwarding of pci devices.
    cmd.insert(0, "sudo")

    process = None
    rc = 0
    try:
        process = subprocess.Popen(cmd, stdin=sys.stdin)
        rc = process.wait()
    except KeyboardInterrupt as e:
        if process is None:
            raise e
        else:
            process.send_signal(signal.SIGINT)
            rc = process.wait()
    print(f"Exited qemu with {rc}")

    # Doing this so I don't need to run the entire script as su
    subprocess.run(["make", "stop-qemu"], check=True)
    # teardown_bridge()

if __name__ == "__main__":
   main()
