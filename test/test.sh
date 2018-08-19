#!/bin/sh

worked=0
for t in $(find . -name '*_test.sh'); do
	sh ${t} >/dev/null
	if [ ${?} -ne 0 ]; then
		echo "${t} failed" >&2
		worked=1
	fi
done

exit ${worked}
