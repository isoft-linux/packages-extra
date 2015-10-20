# This shell script is run before Openbox launches.
# Environment variables set here are passed to the Openbox session.

# Load unisettings to restore user settings from last showdown/reboot.
start-pulseaudio-x11 &
unisettings load &
# Set a background color
if [ -r "/usr/share/slim/themes/default/background.jpg" ]; then
    hsetroot -fill /usr/share/slim/themes/default/background.jpg 
else
    hsetroot -solid "#303030"
fi
#switch touchpad off
/usr/bin/synclient TouchpadOff=1

# D-bus
if which dbus-launch >/dev/null && test -z "$DBUS_SESSION_BUS_ADDRESS"; then
       eval `dbus-launch --sh-syntax --exit-with-session`
fi

# Run XDG autostart things.  By default don't run anything desktop-specific
# See xdg-autostart --help more info
DESKTOP_ENV="OPENBOX"
if which /usr/share/openbox/xdg-autostart >/dev/null; then
  /usr/share/openbox/xdg-autostart $DESKTOP_ENV
fi
