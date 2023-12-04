import os

import subprocess

def main():
    output = subprocess.run(["lspci", "-n", "-D", "-d", "1e52:"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)

    subprocess.run(["modprobe", "vfio-pci"], check=True)

    devices_to_map = []
    for device in output.stdout.splitlines():
        device = device.decode().strip()
        id = device.split()[0]
        vendor = device.split()[2].split(":")
        print(device)
        print(id)

        # ls -l /sys/bus/pci/devices/0000:06:0d.0/iommu_group/devices
        output = subprocess.run(["ls", f"/sys/bus/pci/devices/{id}/iommu_group/devices"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)

        assert len(output.stdout.decode().splitlines()) == 1, output.stdout.decode()

        # readlink /sys/bus/pci/devices/0000:06:0d.0/iommu_group
        subprocess.run(["readlink", f"/sys/bus/pci/devices/{id}/iommu_group"])

        devices_to_map.append((device, id, vendor))

    for (device, id, vendor) in devices_to_map:
        with open(f"/sys/bus/pci/devices/{id}/driver/unbind", "w") as file:
            file.write(id)
        with open("/sys/bus/pci/drivers/vfio-pci/new_id", "w") as file:
            file.write(" ".join(vendor))

if __name__ == "__main__":
    main()
