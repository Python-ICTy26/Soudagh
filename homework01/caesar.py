import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
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
    plaintext = ""

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
    best_shift = 0

    if ciphertext in dictionary:
        return best_shift

    while best_shift <= 24:
        plaintext = decrypt_caesar(ciphertext, best_shift)
        if plaintext in dictionary:
            return best_shift

        best_shift += 1
    return best_shift
