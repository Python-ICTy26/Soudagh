def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE

    d = {}
    start, end = ord('a'), ord('z') + 1
    for i in range(start, end):
        d[chr(i)] = i - start

    while len(plaintext) > len(keyword):
        keyword += keyword

    keyword = keyword.lower()

    for i in range(len(plaintext)):
        ch = ord(plaintext[i])
        shift = d[keyword[i]]
        print(shift)
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


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    d = {}
    start, end = ord('a'), ord('z') + 1
    for i in range(start, end):
        d[chr(i)] = i - start
    print(d)

    while len(ciphertext) > len(keyword):
        keyword += keyword

    keyword = keyword.lower()

    for i in range(len(ciphertext)):
        ch = ord(ciphertext[i])
        shift = d[keyword[i]]
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
