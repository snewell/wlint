#!/bin/sh

current_dir=$(dirname ${0})
current_script=$(basename ${0})

input="${current_dir}/${current_script}.in"
python3 ${WLINT_TOOL_DIR}/count-words.py ${input} |
	tail -n +2 |
	diff "${current_dir}/${current_script}.out" -
