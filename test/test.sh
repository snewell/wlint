#!/bin/sh

base_name=$(dirname ${0})

export WLINT_BASE_DIR="${base_name}/.."
export WLINT_TOOL_DIR="${WLINT_BASE_DIR}/libexec/wlint"
export PYTHONPATH="${PYTHONPATH}:${WLINT_BASE_DIR}/lib"

worked=0
for t in $(find . -name '*_test.sh'); do
	sh ${t} >/dev/null
	if [ ${?} -ne 0 ]; then
		echo "${t} failed" >&2
		worked=1
	fi
done

exit ${worked}
