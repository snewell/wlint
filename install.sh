#!/bin/sh

BASENAME=/usr/bin/basename
CAT=/bin/cat
CUT=/usr/bin/cut
DIRNAME=/usr/bin/dirname
ECHO=/bin/echo
INSTALL=/usr/bin/install
RST2MAN=/usr/bin/rst2man.py
RST2HTML=/usr/bin/rst2html.py
SED=/bin/sed

prefix=/usr/local

do_help() {
	${CAT} <<EOF
${0} - Install writing tools

${0} [--prefix=/path/to/install]

OPTIONS
  -h, --help        Display this help message

  --prefix=<prefix> Install the tools to <prefix>.  This will override DESTDIR
                    if both are set.  Defaults to ${prefix}.

ENVIRONMENT
  DESTDIR
    The prefix for installation.  This can be overriden using the "--prefix"
    option.
EOF
}

basedir=$(${DIRNAME} "${0}")

install_file() {
	file="${1}"
	dest="${2}"
	mode="${3}"

	${INSTALL} -m ${mode} "${file}" "${prefix}/${dest}"
}

install_exec() {
	dest=$(${BASENAME} "${1}" | ${CUT} -d . -f 1)
	install_file "${1}" "${2}/${dest}" "0755"
}

install_share() {
	dest=$(${BASENAME} "${1}")
	install_file "${1}" "${2}/${dest}" "0644"
}

install_directory() {
	${INSTALL} -m 0755 -d "${prefix}/${1}"
}

install_html() {
	dest=$(${BASENAME} "${1}" | ${CUT} -d . -f 1)
	${SED} '/.. BEGIN_MAN_SECTION/,/.. END_MAN_SECTION/d' "${1}" |
		${RST2HTML} > "${prefix}/${2}/wlint-${dest}.html"
}

install_man() {
	dest=$(${BASENAME} "${1}" | ${CUT} -d . -f 1)
	${RST2MAN} "${1}" > "${prefix}/${2}/wlint-${dest}.1"
}

install_helper() {
	runner="${1}"
	path="${2}"
	install_directory "${path}"

	shift 2
	for f in ${@}; do
		"${runner}" "${f}" "${path}"
	done
}

# Check for environmental overrides
if [ -n "${DESTDIR}" ]; then
	prefix=${DESTDIR}
fi

for arg in ${@}; do
	case "${arg}" in
	"--help")
		do_help
		exit ${?}
		;;

	"-h")
		do_help
		exit ${?}
		;;

	"--prefix="*)
		prefix=$(${ECHO} ${arg} | ${CUT} -d = -f 2)
		;;
	esac
done

${ECHO} "Instaling to \"${prefix}\""

binFiles=" \
	bin/wlint.sh \
"
libexecFiles=" \
	libexec/wlint/count-words.py \
	libexec/wlint/list-filter.py \
	libexec/wlint/punctuation-style.py \
"
libWtoolLists=" \
	lib/wlint/__init__.py \
	lib/wlint/common.py \
	lib/wlint/filter.py \
	lib/wlint/punctuation.py \
"
filterLists=" \
	share/wlint/filter-lists/filter-words.txt \
	share/wlint/filter-lists/thought-words.txt \
	share/wlint/filter-lists/weasel-words.txt \
"

# tools
install_helper install_exec "bin" ${binFiles}
install_helper install_share "lib/wlint/" ${libWtoolLists}
install_helper install_exec "libexec/wlint" ${libexecFiles}
install_helper install_share "share/wlint/filter-lists" ${filterLists}

documentationLists=" \
	docs/wlint/count-words.rst \
	docs/wlint/list-filter.rst \
	docs/wlint/punctuation-style.rst \
"

extraFiles=" \
	COPYING \
	README.rst \
"

docDir="share/doc/wlint"
# docs
install_helper install_man "share/man/man1" ${documentationLists}
install_helper install_share "${docDir}" ${extraFiles}
install_helper install_html "${docDir}/html" ${documentationLists}
