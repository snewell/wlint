#!/bin/sh

CAT=/bin/cat
CUT=/usr/bin/cut
DIRNAME=/usr/bin/dirname
ECHO=/bin/echo
LS=/bin/ls
PWD=/bin/pwd

basename=$(${DIRNAME} "${0}")
first=$(${ECHO} ${basename} | ${CUT} -b 1)
if [ "${first}" != "/" ]; then
    basename="$(${PWD})/${basename}"
fi
toolsDir="${basename}/../libexec/writing-tools"

do_help() {
    ${CAT} <<EOF
${0} - Front-end to writing-tools

${0} <tool> [tool options]

OPTIONS
  -h, --help  Display this help message

  --list      List the available tools
EOF
}

do_list() {
    for tool in $(${LS} "${toolsDir}"); do
        if [ -x "${toolsDir}/${tool}" ]; then
            ${ECHO} "${tool}"
        fi
    done
}


if [ ${#} -gt 0 ]; then
    case "${1}" in
      "--help")
        do_help
        exit ${?}
        ;;

      "-h")
        do_help
        exit ${?}
        ;;

      "--list")
        do_list
        exit ${?}
        ;;
    esac
    tool="${toolsDir}/${1}"
    if [ -x "${tool}" ]; then
        shift
        ${tool} ${@}
    else
        ${ECHO} "\"${1}\" - Unknown command" >&2
        exit 1
    fi
else
    do_help
fi
