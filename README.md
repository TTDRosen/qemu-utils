# QEMU Playground

This is really something that I'm using to test cards on emulated targets...

A lot of the basics of setting up qemu can be found at https://yyz-gitlab.local.tenstorrent.com/tenstorrent/syseng-infra/-/wikis/KVM-Guest-with-PCI-Passthrough

## Starting the Image

### Dependencies

To run the Makefile you need psutil and qemu
```bash
pip3 install psutil
sudo apt update && sudo apt install -y qemu-utils qemu-system-misc
```

To use this repo you need a semi recent version of qemu. So if you get any errors you may have to build qemu yourself (fortunatly this is straight forward).

```bash
sudo apt update && sudo apt install -y git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build libcapstone-dev sudo apt install meson libglib2.0-dev valgrind
```

After getting the build dependencies build and install libslirp (this will allow networking to work)

```bash
git clone https://gitlab.com/qemu-project/libslirp.git
cd libslirp
git checkout v4.7.0
meson build
sudo ninja -C build install
```

Then build and install qemu

```bash
wget https://download.qemu.org/qemu-8.2.0-rc2.tar.xz
tar xvJf qemu-8.2.0-rc2.tar.xz
cd qemu-8.2.0-rc2
./configure --enable-slirp
make
sudo make install
```

### Running

To start the riscv image run `make` in the root of the repo.

#### Riscv

If you want to connect via ssh you need to wait for the ssh service to be started.

The default user is ubuntu
The default password is ubuntu

To login via ssh use localhost:10022
To quit (and return pci devices to host) press ctrl-a x

## Setting up TT software

### Inital Config

Hopefully a temporary section, but the default Ubutnu 23.10 install doesn't actually work with Rust. So we have to do a few updates for things to work.

```bash
sudo apt install -y linux-image-6.5.0-14-generic linux-headers-6.5.0-14-generic
sudo reboot
```

### Driver

To start the image won't have the driver or dkms, to install those run

```bash
sudo apt update
sudo apt install -y dkms
wget https://github.com/tenstorrent/tt-kmd/releases/download/ttkmd-1.26/install_ttkmd_1.26.bash
chmod +x ./install_ttkmd_*.bash
sudo ./install_ttkmd_*.bash
```

Once installed you can run lspci to check the the tt cards are use the "tenstorrent" driver.

Or just ensure that /dev/tenstorrent is populated with files for each card.

### TT-SMI

Now install tt-smi (for ease of use it's easiest to just use the provided binary)

First install the python and rust dependencies

```bash
sudo apt install -y python3-pip python3-venv
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
```

Then install tt-smi itself

```
python3 -m venv .env
. ./.env/bin/activate
CARGO_BUILD_TARGET=riscv64gc-unknown-linux-gnu pip install git+https://github.com/tenstorrent/tt-smi
```

Now you can run `tt-smi` as normal.

