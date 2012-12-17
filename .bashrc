#
# default .bashrc
# modified: 6-Jan-2011 by Kevin Heard
#

#
# source the central .bashrc
#
if [ -f /usr/local/skel/local.bashrc ] ; then
        . /usr/local/skel/local.bashrc
fi

#export JAVA_HOME='/usr/'
#export CLASSPATH="/home/corey.hyllested/twitter/t4j/:$CLASSPATH"
export PYTHONPATH="/groups/microfinance/pandas-0.9.0"
#export PATH=$PATH:/home/corey.hyllested/twitter/pig/bin
unalias rm
alias ls='ls --color=auto'

set +o noclobber


function git_branch {
          git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

function proml {
        local BLUE="\[\033[0;34m\]"
        local RED="\[\033[0;31m\]"
        local LIGHT_RED="\[\033[1;31m\]"
        local GREEN="\[\033[0;32m\]"
        local LIGHT_GREEN="\[\033[1;32m\]"
        local WHITE="\[\033[1;37m\]"
        local LIGHT_GRAY="\[\033[0;37m\]"
        local DEFAULT="\[\033[0m\]"

        case $TERM in
                xterm*)
                        TITLEBAR='\[\033]0;\u@\h:\w\007\]';;
                        #TITLEBAR="$(BLUE)\u@\h:\w\007\]";;
                *)
                        TITLEBAR="";;
        esac
        PS1="${TITLEBAR}cah@\h:\W$BLUE \$(git_branch)${DEFAULT}$ "
        PS2='> '
        PS4='+ '
}

proml
