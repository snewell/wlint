#!/bin/sh

current_dir=$(dirname ${0})
current_script=$(basename ${0})

wlint list-filter --sort=sequential \
	<"${current_dir}/${current_script}.in" |
	diff -q "${current_dir}/${current_script}.out" -
