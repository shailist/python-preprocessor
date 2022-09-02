from codecs import register, CodecInfo, IncrementalDecoder
from encodings import utf_8

def reverse_utf_8_encode(input, errors='strict'):
    reversed = input[::-1]
    encoded, size = utf_8.encode(reversed, errors)
    return encoded, size

def reverse_utf_8_decode(input, errors='strict'):
    decoded, size = utf_8.decode(input, errors)
    un_reversed = decoded[::-1]
    return un_reversed, size

class ReverseUTF8IncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, input, final=False):
        self.buffer += input
        
        if final:
            buffer = self.buffer
            self.buffer = b''
            
            decoded, size = reverse_utf_8_decode(buffer)
            return decoded
        
        return ''

@register
def search_function(encoding_name):
    encoding_name = encoding_name.replace('_', '-')
    if encoding_name in 'reverse-utf-8':
        return CodecInfo(
            name='reverse-utf-8',
            encode=reverse_utf_8_encode,
            decode=reverse_utf_8_decode,
            incrementaldecoder=ReverseUTF8IncrementalDecoder
        )


if __name__ == '__main__':
    input = 'Hello world!'
    encoded = input.encode('reverse-utf-8')
    decoded = encoded.decode('reverse-utf-8')

    print(f'Input: {input!r}')
    print(f'Encoded: {encoded!r}')
    print(f'Decoded: {decoded!r}')
