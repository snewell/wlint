punctuation-style
=================

-----------------------------------
check for common punctutaion issues
-----------------------------------

.. BEGIN_MAN_SECTION

:Author: Stephen Newell
:Copyright: BSD Two-Clause
:Version: 0.1.0
:Manual section: 1
:Manual group: wlint manual

.. END_MAN_SECTION


Synopsis
--------
:code:`punctuation-style [options] [file [file ...]]`


Description
-----------
Any punctuation style issues detected will be displayed with line and column
offsets.

::

    sample-input.txt-3533:47 missing space (opening quotes)
    sample-input.txt-4129:44 missing space (opening quotes)
    sample-input.txt-4136:0 missing space (opening quotes)
    sample-input.txt-5521:23 missing space (closing quotes)

If no files are specified, input is read via standard input.


Options
-------
-h, --help          Show this help message and exit.
--file FILE         Process a file. This is only necessary if an input file
                    matches an argument (e.g., --help).
--enable ENABLE     Rules to use when processing text. An asterisk (*) can
                    be used for wildcard matching. [Default: all rules]
--disable DISABLE   Rules to disable when processing text. If a rule is both
                    enabled and disabled, disable takes precedence.


Checks
------
Checks are named are prefixed with a general-purpose name followed by the
specific issue.  When enabling and disabling rules, disabling takes precedence
if there's a conflict.

An asterisk (*) can be used for wildcard matching in rule patterns.  For
example, endash.* will match any rule starting with ``endash.``.

:colon.missing-space:
    Detect cases where a colon (:) isn't followed by a space (e.g.,
    text:text). This can be corrected by adding a space after the colon.
:colon.preceeding-space:
    Detect cases where a colon has a preceeding space (e.g., text : text).
    This can be fixed by removing the space before the colon.

:emdash.preceeding-space:
    Detect cases where an emdash (—) has a preceeding space (e.g., I like
    pancakes —waffles are good too.).  Fix by removing the space.
:emdash.replace-double-hyphen:
    Detect two consecutive hyphens (--).  This is a common convention to
    represent an em-dash (—), so the proper glyph should be used directly.
:emdash.trailing-space:
    Detect cases where an emdash (—) has a trailing space (e.g., I like
    pancakes— waffles are good too.).  Fix by removing the space.

:endash.preceeding-space:
    Detect cases where an endash (–) has a preceeding space (e.g., 24 –30).
    Fix by removing the space.
:endash.replace-emdash:
    Detect cases where a hyphen (-) is used to represent a range instead of an
    endash (–).  This issue can be corrected by replacing the hyphen with an
    endash.
:endash.replace-hyphen:
    Similar to **endash.replace-emdash**, but checks for emdashes (—).
:endash.trailing-space:
    Detect cases where an endash (–) is followed by a space (e.g., 24– 30).
    Fix by removing the space.

:quotation.consecutive-closing-quotes:
    Detect two closing sinqle quotes (’’).  Fix by using an closing double
    quote (”).
:quotation.consecutive-opening-quotes:
    Similar to **quotation.consecutive-closing-quotes**, but checks for two
    opening sinqle quotes (‘‘).  Fix by using an opening double quote (“).
:quotation.incorrect-space-closing-double-single:
    Detect a case where a closing double quote is separated from a closing
    single quote (”’) with something other than a non-breaking thin space ( ).
    Fix by keeping *only* the non-breaking thin space.

    Similar rules exist for this same problem with other quotation
    combinations.  See **quotation.incorrect-space-closing-single-double**,
    **quotation.incorrect-space-opening-double-single**, and
    **quotation.incorrect-space-opening-single-double**.
:quotation.missing-space-closing-double-single:
    Detect a case where a closing double quote is immediately followed by a
    closing single quote (”’).  Fix by adding a non-breaking thin space ( )
    between the quotes.  Note that some fonts may *not* require this space if
    they have sufficient kerning between the glyphs.

    Similar rules exist for this same problem in other combinations.  See
    **quotation.missing-space-closing-single-double**,
    **quotation.missing-space-opening-double-single**, and
    **quotation.missing-space-opening-single-double**.

:semicolon.missing-space:
    See **colon.missing-space**.
:semicolon.preceeding-space:
    See **colon.preceeding-space**.

:time.missing-periods:
    A string that looks like a time is missing the periods in the a.m./p.m.
    section (e.g., 10:00 am).  Fix by adding the periods (10:00 a.m.).
:time.missing-space:
    A string that looks like a time is missing a space between the numeric time
    and the a.m./p.m. (e.g., 10:00a.m.).  Fix by adding a space (10:00 a.m.).
:time.uppercase-APM:
    A string that looks like a time uses uppercase letters in the a.m./p.m.
    section (e.g., 10:00 A.M.).  Fix by using lowercase letters.

    Similar rules exist to detect inconsistent capitalizaiton within a time.
    See **time.uppercase-APm** and **time.uppercase-apM**.
