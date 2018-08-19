#!/bin/sh

current_dir=$(dirname ${0})
current_script=$(basename ${0})

input="${current_dir}/${current_script}.in"
wlint list-filter --lists= ${input} |
	sed "s^${input}^<stdin>^g" |
	diff "${current_dir}/${current_script}.out" -
