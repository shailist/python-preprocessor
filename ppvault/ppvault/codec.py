from base64 import b64decode
from codecs import register, CodecInfo
from encodings import utf_8
from . import ppvault


ENCODING_NAME = 'vault'
_current_password = None


def ppvault_decode(input, errors='strict'):
    global _current_password
    
    decoded, size = utf_8.decode(input, errors)
    
    input_lines = decoded.splitlines()
    output_lines = []
    
    i = 0
    while i < len(input_lines):
        line = input_lines[i]
        
        if line.startswith('#set_password'):
            _current_password = line.split(' ', 1)[1]
        
        elif line == '#vault_start':
            data = input_lines[i + 1]
            if input_lines[i + 2] != '#vault_end':
                raise SyntaxError('#vault_end not found (must be 2 lines after #vault_start)')
            i += 2
            
            if _current_password is not None:
                plain_data = ppvault.try_open_vault(b64decode(data), _current_password)
                output_lines += utf_8.decode(plain_data)[0].splitlines()
                _current_password = None
        
        else:
            output_lines.append(line)
                
        i += 1
    
    output = '\n'.join(output_lines)
    return output, size


class IncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, input, final=False):
        self.buffer += input
        
        if final:
            buffer = self.buffer
            self.buffer = b''
            
            decoded, size = ppvault_decode(buffer)
            return decoded
        
        return ''

@register
def search_function(encoding_name):
    encoding_name = encoding_name.replace('_', '-')
    if encoding_name in ENCODING_NAME:
        return CodecInfo(
            name=ENCODING_NAME,
            encode=utf_8.encode,
            decode=ppvault_decode,
            incrementaldecoder=IncrementalDecoder
        )
