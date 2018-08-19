#!/bin/sh

current_dir=$(dirname ${0})
current_script=$(basename ${0})

input="${current_dir}/${current_script}.in"
wlint count-words ${input} |
	tail -n +2 |
	diff "${current_dir}/${current_script}.out" -
