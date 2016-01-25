"""
Message decoding
"""
import re
import sms.unaccent

pat = re.compile('00[0123456789ABCDEF]{2}')


def decode_unicode(message):
    """
    Decodes a unicode encoded message

    Raises a ValueError if the message can't be decoded
    """
    result = ''
    for index in range(0, len(message), 4):
        word = message[index:index + 4]
        match = pat.match(word)
        if match is None:
            raise ValueError('Message is not unicode')
        result += unichr(int(word, 16))
    return result


# this list was created by reverse engineering, I have no idea if it
# corresponds to any standard or not

accents = {
    '\x80': '\xc7',
    '\x81': '\xfc',
    '\x82': '\xe9',
    '\x83': 'a',
    '\x84': '\xe4',
    '\x85': '\xe0',
    '\x86': '\xe5',
    '\x87': '\xc7',
    '\x88': 'e',
    '\x89': 'e',
    '\x8a': '\xe8',
    '\x8b': 'i',
    '\x8c': 'i',
    '\x8d': '\xec',
    '\x8e': '\xc4',
    '\x8f': '\xc2',
    '\x90': '\xc9',
    '\x91': '\xe6',
    '\x92': '\xc6',
    '\x93': 'o',
    '\x94': '\xf6',
    '\x95': '\xf2',
    '\x96': 'u',
    '\x97': '\xf9',
    '\x98': 'y',
    '\x99': '\xd6',
    '\x9a': '\xdc',
    '\x9b': '',
    '\x9c': '\xa3',
    '\x9d': '\xa5',
    '\x9e': '',
    '\x9f': '',
    '\xa4': '\xf1',
    '\xa5': '\xd1',
}


def decode_accents(message):
    """
    Decode accented characters mixed into ascii message
    """
    result = ''
    for char in message:
        if char in accents:
            result += accents[char]
        else:
            result += str(char, 'ascii', 'replace')
    return result


def to_ascii(text):
    """
    Turn unicode into acsii by unaccenting
    """
    map = sms.unaccent.unaccented_map()
    return text.translate(map).encode('ascii', 'replace')
