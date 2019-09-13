import collections


def cipher_simple(ordinal, steps):
    shifted = ordinal + (steps % (128 - 32))
    if shifted > 127:
        return shifted - (128 - 32)
    if shifted < 0x20:
        return shifted + (128 - 32)
    return shifted

__file_cipher = list(range(0x30, 0x3A)) + list(range(0x61, 0x7B)) + list(map(ord, '_- '))
def cipher_file(ordinal, steps):

    shifted = __file_cipher.index(ordinal) + (steps % len(__file_cipher))
    if shifted >= len(__file_cipher):
        shifted -= len(__file_cipher)
    if shifted < 0:
        shifted += len(__file_cipher)

    return __file_cipher[shifted]


class Cipher:

    def __init__(self, index: int, shifter: callable = None):
        """
        Create a new cipher disk.

        :index int: the key of the cipher
        :disk list optional: a list of all available values (default ascii)
        """

        self.index = index
        if shifter is None:
            self._shifter = cipher_simple
        else:
            self._shifter = shifter
        


    def encode(self, text: collections.Iterable) -> list:
        if isinstance(text, str):
            text = map(ord, text)

        return [self._shifter(i, self.index) for i in text]

    def encodeStr(self, text: str) -> str:
        return ''.join(map(chr, self.encode(text)))

    def decode(self, text: collections.Iterable) -> list:
        if isinstance(text, str):
            text = map(ord, text)

        return [self._shifter(i, -self.index) for i in text]

    def decodeStr(self, text: str) -> str:
        return ''.join(map(chr, self.decode(text)))
