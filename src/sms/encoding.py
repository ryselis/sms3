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
    result = u''
    for index in range(0, len(message), 4):
        word = message[index:index+4]
        match = pat.match(word)
        if match is None:
            raise ValueError('Message is not unicode')
        result += unichr(int(word, 16))
    return result



# this list was created by reverse engineering, I have no idea if it
# corresponds to any standard or not

accents = {
    '\x80': u'\xc7',
    '\x81': u'\xfc',
    '\x82': u'\xe9',
    '\x83': u'a',
    '\x84': u'\xe4',
    '\x85': u'\xe0',
    '\x86': u'\xe5',
    '\x87': u'\xc7',
    '\x88': u'e',
    '\x89': u'e',
    '\x8a': u'\xe8',
    '\x8b': u'i',
    '\x8c': u'i',
    '\x8d': u'\xec',
    '\x8e': u'\xc4',
    '\x8f': u'\xc2',
    '\x90': u'\xc9',
    '\x91': u'\xe6',
    '\x92': u'\xc6',
    '\x93': u'o',
    '\x94': u'\xf6',
    '\x95': u'\xf2',
    '\x96': u'u',
    '\x97': u'\xf9',
    '\x98': u'y',
    '\x99': u'\xd6',
    '\x9a': u'\xdc',
    '\x9b': u'',
    '\x9c': u'\xa3',
    '\x9d': u'\xa5',
    '\x9e': u'',
    '\x9f': u'',
    '\xa4': u'\xf1',
    '\xa5': u'\xd1',
    }
    
def decode_accents(message):
    """
    Decode accented characters mixed into ascii message
    """
    result = u''
    for char in message:
        if char in accents:
            result += accents[char]
        else:
            result += unicode(char, 'ascii', 'replace')
    return result

def to_ascii(text):
    """
    Turn unicode into acsii by unaccenting
    """
    map = sms.unaccent.unaccented_map()
    return text.translate(map).encode('ascii', 'replace')
