all: start-qemu

start-qemu:
	sudo python3 ./setup_vfio.py
	python3 ./start_qemu.py riscv

stop-qemu:
	sudo python3 ./disable_vfio.py
