#!/bin/sh

CUT=/usr/bin/cut
DIRNAME=/usr/bin/dirname
ECHO=/bin/echo
PWD=/bin/pwd

basename=$(${DIRNAME} "${0}")
first=$(${ECHO} ${basename} | ${CUT} -b 1)
if [ "${first}" != "/" ]; then
    basename="$(${PWD})/${basename}"
fi
toolsDir="${basename}/../libexec/writing-tools"

if [ ${#} -gt 0 ]; then
    tool="${toolsDir}/${1}"
    if [ -x "${tool}" ]; then
        shift
        ${tool} ${@}
    fi
fi
