all: start-qemu

start-qemu:
	python3 ./setup_vfio.py
	python3 ./start_qemu.py riscv

stop-qemu:
	python3 ./disable_vfio.py
