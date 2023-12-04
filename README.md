# QEMU Playground

This is really something that I'm using to test cards on emulated targets...

A lot of the basics of setting up qemu can be found at https://yyz-gitlab.local.tenstorrent.com/tenstorrent/syseng-infra/-/wikis/KVM-Guest-with-PCI-Passthrough

## Starting the Image

To start the riscv image run `make` in the root of the repo.

#### Riscv

If you want to connect via ssh you need to wait for the ssh service to be started.

The default user is ubuntu
The default password is ubuntu

To login via ssh use localhost:10022
To quit (and return pci devices to host) press ctrl-a x

## Setting up TT software

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
pip install git+https://github.com/tenstorrent/tt-smi
```

