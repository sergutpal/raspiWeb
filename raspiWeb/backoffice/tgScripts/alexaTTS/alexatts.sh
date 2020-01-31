DEFAULTVOL=80
#EMAIL="XXXXX"
#PASSWORD="XXXX"
#MFA_SECRET="XXXX"
AMAZON="amazon.es"
ALEXA="alexa.amazon.es"
LANGUAGE="es-ES"
#BROWSER=${BROWSER:-$SET_BROWSER}
#CURL=${CURL:-$SET_CURL}
#OPTS=${OPTS:-$SET_OPTS}
#TTS_LOCALE=${TTS_LOCALE:-$SET_TTS_LOCALE}
TMP="/home/nfs/telegram/tgScripts/alexaTTS/tmp"
#OATHTOOL=${OATHTOOL:-$SET_OATHTOOL}
SPEAKVOL=DEFAULTVOL
#NORMALVOL=80
#DEVICEVOLNAME=${DEVICEVOLNAME:-$SET_DEVICEVOLNAME}
#DEVICEVOLSPEAK=${DEVICEVOLSPEAK:-$SET_DEVICEVOLSPEAK}
#DEVICEVOLNORMAL=${DEVICEVOLNORMAL:-$SET_DEVICEVOLNORMAL}

if [ -z "$1" ]; then
    echo -e "\nDebes ejecutarme con la siguiente sintaxis: '$0 "texto" "dispositivo" "vol"(0-100)'\n"
    exit 1
fi


if [ -z "$2" ]; then
    DISPOSITIVOS="ALL"
else
    DISPOSITIVOS=$2
fi

if [ -z "$3" ]; then
    SPEAKVOL=$DEFAULTVOL
else
    SPEAKVOL=$3
fi


export AMAZON
export ALEXA
export LANGUAGE
export TMP
export SPEAKVOL
#export NORMALVOL

/home/nfs/telegram/tgScripts/alexaTTS/alexa_remote_control.sh  -d $DISPOSITIVOS -e "speak: $1"

#/home/nfs/telegram/tgScripts/alexaTTS/alexa_remote_control.sh  -a
