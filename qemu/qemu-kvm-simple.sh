#!/bin/sh
exec /usr/bin/qemu-system-x86_64 -machine accel=kvm -m 2048 -net nic,model=ne2k_pci -net user -soundhw ac97 "$@"
