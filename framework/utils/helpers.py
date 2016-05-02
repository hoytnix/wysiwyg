"""Misc. helper functions."""

import re
import hashlib

import unidecode


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Return an ASCII-only slug.

    Taken from FlaskBB. <@shanks>

    :param text: Text to slugify.
    :param delim: Default '-'. Delimiter for whitespace.
    """

    text = unidecode.unidecode(text)
    result = []
    for word in _punct_re.split(text.lower()):
        result.append(word)
    return delim.join(result)


def html_tags(content, tag, attributes=None):
    """Form a HTML tag.

    :content: String between the HTML tags.
    :tag: a literal HTML tag.
    :attributes: a list of tuples in the order of (key, value).
    """

    if attributes:
        attr_expr = '{}="{}"'
        attr_str = ' ' + ' '.join([attr_expr.format(*attr) for attr in attributes])
    else:
        attr_str = ''
    return '<{tag}{attr}>{content}</{tag}>'.format(
        tag=tag,
        content=content,
        attr=attr_str
    )


def debug_print(title, data, extremity=10, char='='):
    """Print helpful debug messages.

    Used for debugging element_dict originally, but may be evolved later.
    """

    # Title-seperator
    sep_s = char * extremity
    title_s = '{} {} {}'.format(sep_s, title, sep_s)

    # Print.
    print('\n' + title_s)
    pprint(data, indent=4, width=80)
    print(title_s + '\n')
