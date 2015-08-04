#!/bin/sh
exec /usr/bin/qemu-system-x86_64 -machine accel=kvm \
    -m 2048 \
    -net nic,model=ne2k_pci -net user \
    -soundhw ac97 \
    -vga qxl -spice port=5900,addr=0.0.0.0,disable-ticketing \
    -readconfig /etc/qemu/ich9-ehci-uhci.cfg \
    -chardev spicevmc,name=usbredir,id=usbredirchardev1 -device usb-redir,chardev=usbredirchardev1,id=usbredirdev1,debug=3 \
    -chardev spicevmc,name=usbredir,id=usbredirchardev2 -device usb-redir,chardev=usbredirchardev2,id=usbredirdev2,debug=3 \
    -chardev spicevmc,name=usbredir,id=usbredirchardev3 -device usb-redir,chardev=usbredirchardev3,id=usbredirdev3,debug=3 \
    -chardev spicevmc,name=usbredir,id=usbredirchardev4 -device usb-redir,chardev=usbredirchardev4,id=usbredirdev4,debug=3 \
    "$@"
