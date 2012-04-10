#!/usr/bin/env python

import collections
import ConfigParser
import io
import logging
import os
import sys


class CConfig(ConfigParser.SafeConfigParser):
    """
    """
    def __init__(self, defaults=None, dict_type=collections.OrderedDict, \
            allow_no_value=False, base=None, user=None, local=None):
        """
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

    def read_base_config(self, base):
        """
        """
        self.readfp(io.BytesIO(base))

    def read_user_config(self, user):
        """
        """
        filename = os.path.expanduser('~/%s' % user)
        if os.path.exists(filename):
            self.read(filename)
        else:
            logging.warning('No user config: %s' % filename)

    def read_local_config(self, local):
        """
        """
        if isinstance(local, (list, tuple)):
            for l in local:
                self.read_local_config(self, l)
        else:
            if os.path.exists(local):
                self.read(local)
            else:
                logging.warning('No local config: %s' % local)

    def pretty_print(self, stream=sys.stdout):
        """
        Shortcut to print configuration contents to stdout
        """
        self.write(stream)
