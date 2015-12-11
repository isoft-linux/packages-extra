#!/bin/bash
if [ x"$(echo $LANG|grep zh_CN)" = x"$LANG" ]; then
echo "zh"
if [ ! -f $HOME/.config/blender/VERSION/config/userpref.blend ]; then
  mkdir -p $HOME/.config/blender/VERSION/config/
  cp /usr/share/blender/userpref.blend.zh_CN $HOME/.config/blender/VERSION/config/userpref.blend
fi
fi
/usr/share/blender/blender "$@"
