#!/usr/bin/env python

import collections

import cconfig
import cmdconfig


class TypedConfig(cconfig.CConfig):
    """
    A configuration file with parsable types

    Options are in the form:
        name[type]: value

    With default type = str

    See Also
    --------
    CConfig

    """
    def __init__(self, defaults=None, dict_type=collections.OrderedDict, \
            allow_no_value=False, base=None, user=None, local=None):
        """
        Parameters
        ----------

        See Also
        --------
        ConfigParser.SafeConfigParser
        cconfig.CConfig
        """
        self._sdict = dict_type()
        cconfig.CConfig.__init__(self, defaults, dict_type, \
                allow_no_value, base, user, local)
        self.parse()

    def parse(self):
        self._sdict = self._dict()
        for section in self.sections():
            self._sdict[section] = self._dict()
            for option in cconfig.CConfig.options(self, section):
                svalue = cconfig.CConfig.get(self, section, option)
                if ('[' in option) and (']' in option):
                    name, vtype = option.strip(']').split('[')
                    value = eval('%s(%s)' % (vtype, svalue))
                else:
                    value = svalue
                    name = option
                # name, value
                self._sdict[section][name] = value

    def rparse(self, sdict=None):
        if sdict is None:
            sdict = self._sdict
        for (section, options) in sdict.iteritems():
            if section not in self.sections():
                cconfig.CConfig.add_section(self, section)
            for (name, value) in options.iteritems():
                if type(value) == str:
                    cconfig.CConfig.set(self, section, name, value)
                else:
                    option = '%s[%s]' % (name, type(value).__name__)
                    cconfig.CConfig.set(self, section, option, str(value))

    def get(self, section, option):
        return self._sdict[section][option]

    def getint(self, section, option):
        return int(self.get(section, option))

    def getfloat(self, section, option):
        return float(self.get(section, option))

    def getboolean(self, section, option):
        return bool(self.get(section, option))

    def add_section(self, section):
        self._sdict[section] = self._dict()
        self.rparse()

    def has_option(self, section, option):
        return option in self._sdict[section]

    #def has_section(self, section):
    #    pass

    def items(self, section):
        return list(self._sdict[section].iteritems())

    def options(self, section):
        return self._sdict[section].keys()

    #def optionxform(self, optionstr):
    #    pass

    def read(self, filenames):
        cconfig.CConfig.read(self, filenames)
        self.parse()

    def readfp(self, fp, filename=None):
        cconfig.CConfig.readfp(self, fp, filename)
        self.parse()

    def remove_option(self, section, option):
        del self._sdict[section][option]
        self.rparse()

    def remove_section(self, section):
        del self._sdict[section]
        self.rparse()

    #def sections(self):
    #    pass

    def set(self, section, option, value):
        if ('[' in option) and (']' in option):
            name, vtype = option.strip(']').split('[')
            value = eval('%s(%s)' % (vtype, value))
        else:
            name = option
        self._sdict[section][name] = value
        self.rparse()

    def write(self, fp):
        self.rparse()
        cconfig.CConfig.write(self, fp)


class TypedCMDConfig(TypedConfig, cmdconfig.CMDConfig):
    def __init__(self, defaults=None, dict_type=collections.OrderedDict, \
            allow_no_value=False, base=None, user=None, local=None,
            options=None):
        """
        Parameters
        ----------
        options : list of strings, optional
            parsed by CConfig.read_command_line

        See Also
        --------
        ConfigParser.SafeConfigParser
        cconfig.CConfig
        """
        self._sdict = dict_type()
        cmdconfig.CMDConfig.__init__(self, defaults, dict_type, \
                allow_no_value, base, user, local, options)
        self.parse()
