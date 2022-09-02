# Method 1: Using the lookup function:

# from codecs import register, lookup
# 
# @register
# def my_search_function(encoding_name):
#     # Starting with Python 3.9 hyphens are replaced with an underscores
#     if encoding_name in ('my_encoding', 'my-encoding'):
#         return lookup('utf-8')

# Method 2: Building the CodecInfo ourselves

from codecs import register, CodecInfo
from encodings import utf_8

@register
def my_search_function(encoding_name):
    # Starting with Python 3.9 hyphens are replaced with an underscores
    if encoding_name in ('my_encoding', 'my-encoding'):
        return CodecInfo(
            name='my-encoding',
            encode=utf_8.encode,
            decode=utf_8.decode
        )

print('Test'.encode('my-encoding'))
