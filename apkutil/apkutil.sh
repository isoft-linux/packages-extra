#!/bin/sh
shellpath=$(dirname $(readlink -f $0))

deapk() {
    shift
    if test $# -eq 0
    then
        echo "Usage: apkutil deapk [OPTS] <file.apk> [<dir>]"
        echo "        OPTS:"
        echo ""
        echo "        -s, --no-src"
        echo "            Do not decode sources."
        echo "        -r, --no-res"
        echo "            Do not decode resources."
        echo "        -d, --debug"
        echo "            Decode in debug mode. Check project page for more info."
        echo "        -b, --no-debug-info"
        echo "            Baksmali -- don't write out debug info (.local, .param, .line, etc.)"
        echo "        -f, --force"
        echo "            Force delete destination directory."
        echo "        -t <tag>, --frame-tag <tag>"
        echo "            Try to use framework files tagged by <tag>."
        echo "        --frame-path <dir>"
        echo "            Use the specified directory for framework files"
        echo "        --keep-broken-res"
        echo "            Use if there was an error and some resources were dropped, e.g.:"
        echo "            "Invalid config flags detected. Dropping resources", but you"
        echo "            want to decode them anyway, even with errors. You will have to"
        echo "            fix them manually before building."
        exit 0
    fi

    $shellpath/apktool/apktool d $@
}

enapk() {
    shift
    
    if test $# -eq 0
    then
        echo "Usage: apkutil enapk [OPTS] [<app_path>] [<out_file>]"
        echo "        Build an apk from already decoded application located in <app_path>."
        echo ""
        echo "        It will automatically detect, whether files was changed and perform"
        echo "        needed steps only."
        echo ""
        echo "        If you omit <app_path> then current directory will be used."
        echo "        If you omit <out_file> then <app_path>/dist/<name_of_original.apk>"
        echo "        will be used."
        echo ""
        echo "        OPTS:"
        echo ""
        echo "        -f, --force-all"
        echo "            Skip changes detection and build all files."
        echo "        -d, --debug"
        echo "            Build in debug mode. Check project page for more info."
        echo "        -a, --aapt"
        echo "            Loads aapt from specified location."
        echo "        --frame-path <dir>"
        echo "            Use the specified directory for framework files"
        exit 0
    fi

    $shellpath/apktool/apktool b $@
}

inst_framework() {   
    shift
    if test $# -eq 0 
    then
        echo "Usage: apkutil if <framework.apk> [<tag>]"
        echo "   Install framework file to your system."
        exit 0
    fi
    $shellpath/apktool/apktool install-framework $@
}

baksmali() {
    shift
    java -jar $shellpath/smali/baksmali.jar $@
}

smali() {
    shift
    java -jar $shellpath/smali/smali.jar $@
}

rundex() {
    shift
    java -jar $shellpath/dalvikvm/dalvikvm.jar $@
}
dava() {
    shift
    java -cp $shellpath/soot/soot.jar soot.Main -cp /usr/java/default/jre/lib/rt.jar:/usr/java/default/jre/lib/jce.jar:$shellpath/android-4.1-api16/android.jar:. -output-format d $@
}

jar2dex() {
    shift
    $shellpath/dex2jar/d2j-jar2dex.sh $@
}

dex2jar() {
    shift
    $shellpath/dex2jar/d2j-dex2jar.sh $@
}
droiddraw() {
    shift
    java -jar $shellpath/droiddraw/droiddraw.jar $@
}
installagent() {
    adb install $shellpath/droiddraw/androiddraw-signed.apk
    echo "You need call \"apkutil agentforward\" to set a forward rule of droiddraw agent"
}
agentforward() {
    adb forward tcp:6100 tcp:7100
}
sign() {
    shift

    if test $# -ne 2
    then
        echo "Usage: apkutil sign input.apk output.apk"
        exit 0
    fi
    java -jar $shellpath/signapk/signapk.jar $shellpath/signapk/testkey.x509.pem $shellpath/signapk/testkey.pk8 $@
}


setdevice()
{
    shift
    if test $# -ne 1
    then
        echo "Please use \"/usr/sbin/lsusb\" to find your device and get the vendor ID"
        echo "For example, if you get \"Bus 002 Device 005: ID 1d91:3f04\""
        echo "The 1d91 is the vendor ID"
        echo "and run \"apkutil setdevice 1d91\" again"
        exit 1
    fi
    mkdir -p ~/.android
    echo "0x$@" >~/.android/adb_usb.ini
    echo "Done"
    echo "Please run \"apkutil adb kill-server\""
    echo "And \"apkutil adb devices\""
    echo "To find your new device"
}

runadb()
{
    shift
    adb $@
}

adbshell()
{
    shift
    adb shell
}

adbpush()
{
    shift
    adb push $@ 
}

adbrun()
{
    shift
    adb shell su -c \"$@\"
}

runzipalign()
{
    shift
    zipalign $@
}

dx()
{
    shift
    $shellpath/dx/dx $@
}

compile()
{
    shift
        export CLASSPATH=$CLASSPATH:$shellpath/android-4.1-api16/android.jar
        javac -source 1.6 -target 1.6 $@
}

runaapt()
{
    shift
    aapt $@
}

runaidl()
{
    shift
    aidl $@
}

gen_r_java() {
    shift
    if test $# -eq 0 
    then
        echo "Usage: apkutil genrjava <path>"
        echo "   generate R.java and store it under <path>/<package path>"
        exit 0
    fi
    aapt package -f -m -S res -I $shellpath/android-4.1-api16/android.jar -M AndroidManifest.xml -J $@
}

create_project() {
    read -p "Please input project folder:" project_folder
    read -p "Please input package name:" package_name
    
    package_path=$(echo "$package_name"|sed 's/\./\//g')
    
    #create project folder to hold everything
    mkdir -p "$project_folder"
    #create basic folder layout of project 
    mkdir -p "$project_folder/bin"
    mkdir -p "$project_folder/gen"
    mkdir -p "$project_folder/assets"
    mkdir -p "$project_folder/res/values/"
    mkdir -p "$project_folder/res/layout/"
    mkdir -p "$project_folder/res/drawable/"
    mkdir -p "$project_folder/src/$package_path"
    
    tar zxf $shellpath/template.tar.gz -C "$project_folder/src/$package_path" HelloWorld.java
    tar zxf $shellpath/template.tar.gz -C "$project_folder" res
    tar zxf $shellpath/template.tar.gz -C "$project_folder" AndroidManifest.xml
    tar zxf $shellpath/template.tar.gz -C "$project_folder" apktool.yml
    tar zxf $shellpath/template.tar.gz -C "$project_folder" Makefile
    
    sed -i "s/PACKAGE_NAME/$package_name/g" "$project_folder"/AndroidManifest.xml
    sed -i "s/PACKAGE_NAME/$package_name/g" "$project_folder"/apktool.yml
    sed -i "s/PACKAGE_NAME/$package_name/g" "$project_folder/src/$package_path"/HelloWorld.java
    sed -i "s#PACKAGE_PATH#$package_path#g" "$project_folder"/Makefile
    echo "Done"
}
case "$1" in
    deapk)
        deapk $@ 
    ;;
    enapk)
        enapk $@
    ;;
    if)
        inst_framework $@
    ;;
    baksmali)
        baksmali $@
    ;;
    smali)
        smali $@
    ;;
    dalvikvm)
        rundex $@
    ;;
    dex2jar)
        dex2jar $@
    ;;
    jar2dex)
        jar2dex $@
    ;;
    droiddraw)
        droiddraw $@
    ;;
    installagent)
        installagent $@
    ;;
    agentforward)
        agentforward $@
    ;;
    dava)
        dava $@
    ;;
    sign)
        sign $@
    ;;
    setdevice)
        setdevice $@
    ;;
    adb)
        runadb $@
    ;;
    adbshell)
        adbshell $@
    ;;
    adbpush)
        adbpush $@
    ;;
    adbrun)
        adbrun $@
    ;;
    zipalign)
        runzipalign $@
    ;;
    dx)
        dx $@
    ;;
    javac)
        compile $@
    ;;
    aapt)
        runaapt $@
    ;;
    genrjava)
        gen_r_java $@
    ;;
    aidl)
        runaidl $@ 
    ;;
    create)
        create_project
    ;;
    *)
    echo $"Usage: apkutil <command>"
    echo ""
    echo "command list:"
    echo "  deapk       -- decompile apk file"
    echo "  enapk       -- re-compile directory to apk"
    echo "  if          -- install framework file to your system which needed by apktool"
    echo ""
    echo "  baksmali    -- use baksmali to decode dex file"
    echo "  smali       -- use smali to encode smalis to dex"
    echo "  dalvikvm    -- use pure java dalvikvm to run simple dex file"
    echo ""
    echo "  dex2jar     -- convert dex to jar"
    echo "  jar2dex     -- convert jar to dex"
    echo ""
    echo "  droiddraw   -- GUI builder"
    echo "  installagent-- install droiddraw agent to device"
    echo "  agentforward-- setup agentforward rule"
    echo ""
    echo "  genrjava    -- generate R.java"
    echo "  javac       -- javac wrapper with classpath set to android-4.1 framwork"
    echo "  dava        -- java decompiler"
    echo ""
    echo "  dx          -- dx wrapper"
    echo ""
    echo "  sign        -- sign apk with testkey"
    echo ""
    echo "  setdevice   -- setup device for adb"
    echo "  adb         -- android adb wrapper"
    echo "  adbrun      -- run command with adb"
    echo "  adbshell    -- launch adb shell"
    echo "  adbpush     -- adb push wrapper"
    echo ""
    echo "  zipalign    -- zipalign wrapper"
    echo "  aapt        -- aapt wrapper"
    echo "  aidl        -- aidl wrapper"
    echo ""
    echo "  create      -- create a HelloWorld project via template"
    ;;
esac
