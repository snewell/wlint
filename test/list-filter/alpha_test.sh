#!/bin/sh

current_dir=$(dirname ${0})
current_script=$(basename ${0})

input="${current_dir}/${current_script}.in"
python ${WLINT_TOOL_DIR}/list-filter.py ${input} |
	sed "s^${input}^<stdin>^g" |
	diff "${current_dir}/${current_script}.out" -
