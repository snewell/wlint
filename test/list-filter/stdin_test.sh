#!/bin/sh

current_dir=$(dirname ${0})
current_script=$(basename ${0})

python ${WLINT_TOOL_DIR}/list-filter.py --sort-method=sequential \
	<"${current_dir}/${current_script}.in" |
	diff -q "${current_dir}/${current_script}.out" -
