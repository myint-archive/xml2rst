#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Based on sample.py,v 4.1.2.6 2006/04/14 13:59:26 cvs Exp

# Copyright (C) 2009 Stefan Merten

# xml2rst.py is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

"""Convert a docutils XML file to reStructuredText syntax.

This can be used to transform another format to reStructuredText given you have
a transformation to docutils XML.

"""

from __future__ import print_function


import sys
import os.path
import re

from optparse import OptionParser
from optparse import OptionGroup

from xml2rstlib import rst_xslt


def parseOptions():
    """Sets options and returns arguments.

    @return: Name of input file and optionally of output file.
    @rtype: ( str, [str,] )

    """
    optionParser = OptionParser('usage: %prog [option]... <xml> [<rst>]')

    generalGroup = OptionGroup(optionParser, 'General options')

    generalGroup.add_option('-a', '--adornment', default=None,
                            help="""
Configures title markup to use so different styles can be requested
easily.

The value of the parameter must be a string made up of a sequence of
character pairs. The first character of a pair is C<o> (overline) or
C<u> (underline) and the second character is the character to use for
the markup.

The first and the second character pair is used for document title and
subtitle, the following pairs are used for section titles where the
third pair is used for the top level section title.
""")

    generalGroup.add_option('-f', '--fold', type='int', default=None,
                            help="""
Configures whether long text lines in paragraphs should be folded and
to which length. This option is for input not coming from reST which
may have no internal line feeds in plain text strings.

If folding is enabled text strings not in a line feed preserving
context are first white-space normalized and then broken according to
the folding rules. Folding rules put out the first word and continue
to do so with the following words unless the next word would cross
the folding boundary. Words are delimited by white-space.
""")

    generalGroup.add_option('-v', '--verbose', action='store_true',
                            help='Operate verbose.')
    optionParser.add_option_group(generalGroup)

    argumentGroup = OptionGroup(optionParser, 'Arguments')
    optionParser.add_option_group(argumentGroup)

    argument1Group = OptionGroup(optionParser, 'xml',
                                 'The XML input file containing docutils '
                                 'XML.')
    optionParser.add_option_group(argument1Group)

    argument2Group = OptionGroup(
        optionParser, 'rst',
        'The optional output file containing reStructuredText. '
        'If not given output is put to standard out.')
    optionParser.add_option_group(argument2Group)

    (options, args) = optionParser.parse_args()

    if len(args) < 1:
        optionParser.error('An input file is required')
    if len(args) > 2:
        optionParser.error('At most two arguments are allowed')
    if (options.adornment is not None
        and re.search('^([ou][]!"#$%&\'()*+,\-./:;<=>?@[\\^_`{|}~])+$',
                      options.adornment) is None):
        optionParser.error('Invalid adornment string given')

    return (options, args)


def errorOut(lines):
    """Outputs messages as error.

    @param lines: Messages to be output as single lines.
    @type lines: ( str, ..., )

    @return: 0
    @rtype: int

    """
    scriptName = os.path.basename(sys.argv[0])
    for line in lines:
        print(('%s: %s' % (scriptName, line, )), file=sys.stderr)
    return 0


def errorExit(code, lines):
    """Exit program with an error message.

    @param code: Exit Code to use.
    @type code: int

    @param lines: Strings to output as error message.
    @type lines: ( str, ..., )

    @return: Does not return.

    """
    errorOut(lines)
    sys.exit(code)


if __name__ == '__main__':
    (options, arguments) = parseOptions()
    inF = arguments[0]

    if inF == '-':
        import tempfile
        temporary_file = tempfile.NamedTemporaryFile(mode='w')
        temporary_file.write(sys.stdin.read())
        temporary_file.flush()
        inF = temporary_file.name
    else:
        temporary_file = None

    if len(arguments) > 1:
        outF = arguments[1]
    else:
        outF = None
    try:
        rst_xslt.convert(inF, outF, options)
    except Exception as e:
        errorExit(1, e)
    finally:
        if temporary_file:
            temporary_file.close()


# TODO Accept additional XSLT sheets to create a transformation pipeline

# TODO Move from XSLT to Python implementation step by step by replacing
#      XSLT-code by Python code through extensions and other means


# TODO The docutils XML reader must be used
