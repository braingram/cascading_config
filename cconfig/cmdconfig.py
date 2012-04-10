#!/usr/bin/env python

import collections
import sys

import cconfig


class CMDConfig(cconfig.CConfig):
    """
    A configuration file that also reads in options from the command line

    Options are in the form:
        [section] key value ...

    See Also
    --------
    CMDConfig.read_command_line

    """
    def __init__(self, defaults=None, dict_type=collections.OrderedDict, \
            allow_no_value=False, base=None, user=None, local=None,
            options=sys.argv[1:]):
        """
        Parameters
        ----------
        options : list of strings, optional
            parsed by CMDConfig.read_command_line

        See Also
        --------
        ConfigParser.SafeConfigParser
        cconfig.CConfig
        """
        cconfig.CConfig.__init__(self, defaults, dict_type, \
                allow_no_value, base, user, local)
        self.read_command_line(options)

    def read_command_line(self, options, starting_section='main'):
        """
        Parameters
        ----------
        options : list of strings
            list of options to parse where options keys, values, and
            section changes. If a section name is encountered, all
            subsequent key value pairs will effect only the new section
        starting_section : string, optional
            starting default section

        Raises
        ------
        AttributeError
            if a key is missing a value

        Example
        -------
        options = ['timerange', '0:1000']
            will set main:timerange to '0:1000'

        # if filter and template are sections
        options = ['filter', 'method', 'butter', 'low', '500',
            'template', 'method', 'center']
            will set filter:method to butter, filter:low to 500
                and template:method to center
        """
        section = 'main'
        key = None
        for option in options:
            if option in self.sections():  # change sections
                section = option
                continue
            if key is None:
                key = option
                continue
            val = option.strip()
            if val[0] in ['"', "'"]:
                val = val[1:]
            if val[-1] in ['"', "'"]:
                val = val[:-1]
            self.set(section, key, val)
            key = None
        if key is not None:
            raise AttributeError("Key [%s] missing value [section:%s]" % \
                    (key, section))
