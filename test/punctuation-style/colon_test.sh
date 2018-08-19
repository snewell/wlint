#!/bin/sh

current_dir=$(dirname ${0})
current_script=$(basename ${0})

input="${current_dir}/${current_script}.in"
wlint punctuation-style ${input} |
	sed "s^${input}^<stdin>^g" |
	diff -u "${current_dir}/${current_script}.out" -
