#!/usr/bin/env python

import collections
import ConfigParser
import io
import logging
import os
import sys


class CConfig(ConfigParser.SafeConfigParser):
    """
    A cascading configuration file parser that loads the following
    configuration files:
        base < user < local[s]

    Settings in user will overwrite base, local will overwrite user.
    """
    def __init__(self, defaults=None, dict_type=collections.OrderedDict, \
            allow_no_value=False, base=None, user=None, local=None):
        """
        Parameters
        ----------
        base : string, optional
            base configuration, like the contents of an ini file
        user : string, optional
            user configuration, expanded with os.path.expanduser('~/%s')
        local : string or tuple/list, optional
            single or multiple local configurations

        See Also
        --------
        ConfigParser.SafeConfigParser
        """
        ConfigParser.SafeConfigParser.__init__(self, defaults, dict_type, \
                allow_no_value)
        # process base
        if base is not None:
            self.read_base_config(base)
        # load home
        if user is not None:
            self.read_user_config(user)
        # load local
        if local is not None:
            self.read_local_config(local)
        # process command line
        pass

    def read_string(self, string):
        """
        Parameters
        ----------
        string : str
            string containing sections and options similar to an ini file
        """
        self.readfp(io.BytesIO(string))

    def read_base_config(self, base):
        """
        Parameters
        ----------
        base : file or string
            base configuration, like the contents of an ini file

        See Also
        --------
        read_string
        """
        if hasattr(base, "read"):
            self.readfp(base)
        else:
            self.read_string(base)

    def read_user_config(self, user):
        """
        Parameters
        ----------
        user : file or string
            user configuration, expanded with os.path.expanduser('~/%s')
        """
        if hasattr(user, "read"):
            self.readfp(user)
        else:
            filename = os.path.expanduser('~/%s' % user)
            if os.path.exists(filename):
                self.read(filename)
            else:
                logging.warning('No user config: %s' % filename)

    def read_local_config(self, local):
        """
        Parameters
        ----------
        local : file, string or tuple/list
            single or multiple local configurations
        """
        if isinstance(local, (list, tuple)):
            for l in local:
                self.read_local_config(self, l)
        else:
            if hasattr(local, "read"):
                self.readfp(local)
            else:
                if os.path.exists(local):
                    self.read(local)
                else:
                    logging.warning('No local config: %s' % local)

    def pretty_print(self, stream=sys.stdout):
        """
        Shortcut to print configuration contents to stdout

        Parameters
        ----------
        stream : file pointer
            where to print the configuration
        """
        self.write(stream)
