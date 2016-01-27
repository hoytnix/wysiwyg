#!/usr/bin/env python

"""
anavah.utils.helpers
~~~~~~~~~~~~~~~~~~~~

Misc. helper functions.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

import re

import unidecode


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    '''Returns an ASCII-only slug.
    Taken from FlaskBB. <@shanks>

    :param text: Text to slugify.
    :param delim: Default '-'. Delimiter for whitespace.
    '''

    text = unidecode.unidecode(text)
    result = []
    for word in _punct_re.split(text.lower()):
        result.append(word)
    return delim.join(result)



