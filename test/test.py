#!/usr/bin/env python

import io

import cconfig


def get_assert(c, s, k, v):
    assert c.get(s, k) == v, "[%s]%s{=%s} != %s in %s" \
            % (s, k, c.get(s, k), v, c)

base = """
[main]
a: 1
b: 2
c: 3

[foo]
a: 4
b: 5
c: 6
"""

user = """
[main]
b: 22

[foo]
a: 44
"""

local = """
[main]
c: 33

[foo]
b: 55
"""


def test_cconfig():
    print "CConfig"
    c = cconfig.CConfig(base=io.BytesIO(base), user=io.BytesIO(user), \
            local=io.BytesIO(local))
    c.pretty_print()

    for k, v in (('a', '1'), ('b', '22'), ('c', '33')):
        get_assert(c, 'main', k, v)

    for k, v in (('a', '44'), ('b', '55'), ('c', '6')):
        get_assert(c, 'foo', k, v)


def test_cmdconfig():
    print "CMDConfig"
    args = ["a", "11", "foo", "c", "66"]

    c = cconfig.CMDConfig(base=io.BytesIO(base), user=io.BytesIO(user), \
            local=io.BytesIO(local), options=args)
    c.pretty_print()

    for k, v in (('a', '11'), ('b', '22'), ('c', '33')):
        get_assert(c, 'main', k, v)

    for k, v in (('a', '44'), ('b', '55'), ('c', '66')):
        get_assert(c, 'foo', k, v)


def test_typedconfig():
    print "TypedConfig"
    tbase = base.replace(':', '[int]:')
    tuser = io.BytesIO(user.replace(':', '[int]:'))
    tlocal = io.BytesIO(local.replace(':', '[int]:'))
    c = cconfig.TypedConfig(base=tbase, user=tuser, local=tlocal)
    c.pretty_print()

    for k, v in (('a', '1'), ('b', '22'), ('c', '33')):
        get_assert(c, 'main', k, int(v))

    for k, v in (('a', '44'), ('b', '55'), ('c', '6')):
        get_assert(c, 'foo', k, int(v))


def test_typedcmdconfig():
    print "TypedCMDConfig"
    tbase = base.replace(':', '[int]:')
    tuser = io.BytesIO(user.replace(':', '[int]:'))
    tlocal = io.BytesIO(local.replace(':', '[int]:'))
    args = ["a[int]", "11", "foo", "c[int]", "66"]
    c = cconfig.TypedCMDConfig(base=tbase, user=tuser, local=tlocal, \
            options=args)
    c.pretty_print()

    for k, v in (('a', '11'), ('b', '22'), ('c', '33')):
        get_assert(c, 'main', k, int(v))

    for k, v in (('a', '44'), ('b', '55'), ('c', '66')):
        get_assert(c, 'foo', k, int(v))

if __name__ == '__main__':
    test_cconfig()
    test_cmdconfig()
    test_typedconfig()
    test_typedcmdconfig()
