import subprocess

def main():
    output = subprocess.run(["lspci", "-n", "-D", "-d", "1e52:"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)

    subprocess.run(["modprobe", "tenstorrent"], check=True)

    devices_to_map = []
    for device in output.stdout.splitlines():
        device = device.decode().strip()
        id = device.split()[0]
        vendor = device.split()[2].split(":")
        print(device)
        print(id)

        # echo vvvv dddd > /sys/bus/pci/drivers/vfio-pci/remove_id
        #with open(f"/sys/bus/pci/drivers/vfio-pci/remove_id", "w") as file:
        #    file.write(" ".join(vendor))

        with open(f"/sys/bus/pci/devices/{id}/driver/unbind", "w") as file:
            file.write(id)
        # echo INSERT_PCI_ADDRESS_HERE > /sys/bus/pci/drivers/INSERT_DESIRED_DRIVER_HERE/bind
        with open("/sys/bus/pci/drivers/tenstorrent/bind", "w") as file:
            file.write(id)

if __name__ == "__main__":
    main()
