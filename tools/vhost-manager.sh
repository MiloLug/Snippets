#!/bin/bash
################################## utils
PROGNAME=`basename "$0"`
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
trap 'echo; exit' INT

RET_VALUE=0

#text color modifiers
t_red=`tput setaf 1`
t_green=`tput setaf 2`
t_yellow=`tput setaf 3`
t_reset=`tput sgr0`

#run function if it exists
function try-function {
    if [ "$(LC_ALL=C type -t $1)" = function ]; then
        $1 "${@:2}"
    else
        echo "Error: function $1 does not exist."
    fi
}

#root user checker
function rootcheck () {
    if [ "$(id -u)" != "0" ]
    then
        sudo "$0" "$@"
        exit $?
    fi
}

AGREE_ALL=false
#default prompt
function prompt-selector {
    if $AGREE_ALL ; then
        RET_VALUE=true
        return
    fi
    echo "$1" >&2
    local r=false
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) r=true; break;;
            No ) r=false; break;;
        esac
    done

    RET_VALUE=$r
}

################################## USAGE
usage() {
    echo "\
${t_green}Usage${t_reset}: $PROGNAME [-y] <function-name> [arguments...]

${t_green}Note${t_reset}: the domain name is also the configuration file name

${t_green}Functions${t_reset}:
    ${t_yellow}link-domain${t_reset} <domain-name> <domain-dir> : add a new domain to 
        the apache's configuration.
        Also adds the domain to the /etc/hosts with the 127.0.0.1 redirection.
    
    ${t_yellow}unlink-domain${t_reset} <domain-name> : removes domain from the configurations
        and /etc/hosts.
        ${t_yellow}-y${t_reset} - agree to ${t_green}remove${t_reset} the .conf file

    ${t_yellow}list-domain${t_reset} [enabled/e] : shows all domains in the configs
        ${t_yellow}enabled, e${t_reset} - show only enabled domains

${t_green}Flags${t_reset}:
    ${t_yellow}-y${t_reset}: agree with all possible questions

" >&2
  exit 1
}


################################## script functions


#add new directory as domain
function link-domain {
    if [ $# -lt 2 ]; then
        echo "${t_red}Error${t_reset}: this functuion requires min 2 arguments."
        exit
    fi

	local confName="$1.conf"
    local confPath="/etc/apache2/sites-available/$confName"
    local hostDir=`realpath "$2"` 2>/dev/null 1>/dev/null

    if [ ! -d $hostDir ]; then
        echo "${t_red}Error${t_reset}: the host's directory '$hostDir' does not exist."
        exit
    fi

    if [ -f $confPath ]; then
        echo "$1 already exists."
        echo "I'll try to enable it."
    else
        echo "$1 creation..."
        echo "\
<VirtualHost *:80>
    ServerName $1
    ServerAlias www.$1
    DocumentRoot \"$hostDir\"

    <Directory \"$hostDir\">
        Options -Indexes +FollowSymLinks +MultiViews
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>" > $confPath

        "$SCRIPTPATH/hostess" add $1 127.0.0.1
    fi

    a2ensite $1 2>/dev/null 1>/dev/null
    systemctl reload apache2

    echo "OK"
}

#remove domain
function unlink-domain {
    if [ $# -lt 1 ]; then
        echo "${t_red}Error${t_reset}: this functuion requires min 1 argument."
        exit
    fi

	local confName="$1.conf"
    local confPath="/etc/apache2/sites-available/$confName"

    if [ -f $confPath ]; then
        echo "Removing $1..."
        a2dissite $1 2>/dev/null 1>/dev/null
        systemctl reload apache2

        "$SCRIPTPATH/hostess" rm $1 127.0.0.1 2>/dev/null 1>/dev/null
        echo "hosts: $1 -> 127.0.0.0 has been removed"
        echo
        prompt-selector "Do tou want to remove the .conf file?"
        if $RET_VALUE ; then
            rm "$confPath"
            echo "$confName has been removed"
        fi
    else
        echo "${t_red}Error${t_reset}: the $1 does not exist."
        exit
    fi
}

function list-domain {
    local configsDir="/etc/apache2/sites-available"
    local enablesDir="/etc/apache2/sites-enabled"
    local fStatus=false
    if [ "$1" == "enabled" ] || [ "$1" == "e" ]; then
        configsDir=$enablesDir
        fStatus=true
    fi

    local i=0
    local status=""
    for file in "$configsDir"/*.conf; do
        i=$(( i + 1 ))
        file=`basename $file`
        echo "$i. ${t_green}File name${t_reset}: $file"
        
        awk '/<VirtualHost/ { sn=""; dr="" }
/ServerName/ { sname = $2 }
/DocumentRoot/ { sdir = $2 }
/\/VirtualHost/ {gsub(/"/, "", sname);gsub(/"/, "", sdir); if(length(sname) > 0) print "Host: name = ", sname, "; location = ", sdir; else print "Host: no server name; location = ", sdir; }' "$configsDir/$file"
        if ! $fStatus ; then
            if [ -f "$enablesDir/$file" ] ; then
                status="enabled"
            else
                status="disabled"
            fi
            echo "Status: $status"
        fi
        echo
    done
}

################################## MAIN

#invoke through the root user
rootcheck "${@}"

while getopts y o; do
  case $o in
    (y) AGREE_ALL=true;;
  esac
done
shift "$((OPTIND - 1))"

if [ $# -eq 0 ]; then
    echo "${t_red}Error${t_reset}: no function name."
    echo
    usage
    exit
fi

try-function "$@"
