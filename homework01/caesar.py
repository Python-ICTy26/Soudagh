import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        ch = ord(plaintext[i])
        if 65 <= ch <= 90:
            if ch + shift > 90:
                ciphertext += chr(65 + (shift - (90 - ch)) - 1)
            else:
                ciphertext += chr(ch + shift)
        elif 97 <= ch <= 122:
            if ch + shift > 122:
                ciphertext += chr(97 + (shift - (122 - ch)) - 1)
            else:
                ciphertext += chr(ch + shift)
        else:
            ciphertext += chr(ch)

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    for i in range(len(ciphertext)):
        ch = ord(ciphertext[i])
        if 65 <= ch <= 90:
            if ch - shift < 65:
                plaintext += chr(90 - (shift - (ch - 65) - 1))
            else:
                plaintext += chr(ch - shift)
        elif 97 <= ch <= 122:
            if ch - shift < 97:
                plaintext += chr(122 - (shift - (ch - 97) - 1))
            else:
                plaintext += chr(ch - shift)
        else:
            plaintext += chr(ch)

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
