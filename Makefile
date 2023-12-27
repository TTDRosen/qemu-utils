all: start-qemu

TT_QEMU_ARCH ?= riscv

start-qemu:
	sudo python3 ./setup_vfio.py
	python3 ./start_qemu.py ${TT_QEMU_ARCH}

stop-qemu:
	sudo python3 ./disable_vfio.py

clean-qemu:
	rm -rf .ignore/${TT_QEMU_ARCH}/*
