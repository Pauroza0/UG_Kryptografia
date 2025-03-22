## Paulina Różańska
import argparse
import string
from collections import Counter

ALPHABET = string.ascii_lowercase
ALPHABET_LEN = len(ALPHABET)


ENGLISH_FREQ = [
    82, 15, 28, 43, 127, 22, 20, 61, 70, 2, 8, 40, 24,
    67, 75, 19, 1, 60, 63, 91, 28, 10, 24, 2, 20, 1
]


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip()


def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def przesuniecie(c, znak_klucz, encrypt=True):
    if c not in ALPHABET:
        return c
    offset = ALPHABET.index(znak_klucz)
    index = ALPHABET.index(c)
    if encrypt:
        return ALPHABET[(index + offset) % ALPHABET_LEN]
    else:
        return ALPHABET[(index - offset) % ALPHABET_LEN]


def repeat(key, length):
    return (key * (length // len(key) + 1))[:length]


def encrypt(plain, key):
    key = repeat(key, len(plain))
    return ''.join(przesuniecie(c, k, encrypt=True) for c, k in zip(plain, key))


def decrypt(cipher_text, key):
    key = repeat(key, len(cipher_text))
    return ''.join(przesuniecie(c, k, encrypt=False) for c, k in zip(cipher_text, key))


def czestosc(text):
    counter = Counter(text)
    freq = [0] * ALPHABET_LEN
    for i, c in enumerate(ALPHABET):
        freq[i] = counter.get(c, 0)
    total = sum(freq)
    if total == 0:
        return freq
    return [f * 1000 / total for f in freq]


def iloczyn(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))


def koicydencja(text):
    n = len(text)
    freqs = Counter(text)
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1)) if n > 1 else 0
    return ic


def dlugosc_klucza(cipher_text, max_len=20):
    best_lenght = 1
    best_ic = 0
    for key_len in range(1, max_len + 1):
        ics = []
        for i in range(key_len):
            group = cipher_text[i::key_len]
            ics.append(koicydencja(group))
        avg_ic = sum(ics) / len(ics)
        if avg_ic > best_ic:
            best_ic = avg_ic
            best_lenght = key_len
    return best_lenght


def find_key(cipher_text, key_len):
    key = ''
    for i in range(key_len):
        group = cipher_text[i::key_len]
        max_corr = -1
        best_shift = 0
        for shift in range(ALPHABET_LEN):
            shifted = ''.join(przesuniecie(c, ALPHABET[shift], encrypt=False) for c in group)
            freq = czestosc(shifted)
            corr = iloczyn(freq, ENGLISH_FREQ)
            if corr > max_corr:
                max_corr = corr
                best_shift = shift
        key += ALPHABET[best_shift]
    return key


def main():
    parser = argparse.ArgumentParser(description="Szyfr Vigenère'a")
    parser.add_argument("-p", action="store_true", help="Przygotowanie")
    parser.add_argument("-e", action="store_true", help="Szyfrowanie")
    parser.add_argument("-d", action="store_true", help="Deszyfrowanie")
    parser.add_argument("-k", action="store_true", help="Kryptoanaliza")
    args = parser.parse_args()

    if args.e:
        text = read_file("plain.txt")
        key = read_file("key.txt")
        cipher = encrypt(text, key)
        write_file("crypto.txt", cipher)
    elif args.p:
        orig = read_file("orig.txt")
        characters = set(string.ascii_lowercase)
        plain = ''.join(c for c in orig.lower() if c in characters)
        write_file("plain.txt", plain)
    elif args.d:
        cipher = read_file("crypto.txt")
        key = read_file("key.txt")
        plain = decrypt(cipher, key)
        write_file("decrypt.txt", plain)
    elif args.k:
        cipher = read_file("crypto.txt")
        key_len = dlugosc_klucza(cipher)
        key = find_key(cipher, key_len)
        write_file("key-found.txt", key)
        plain = decrypt(cipher, key)
        write_file("decrypt.txt", plain)
    else:
        print("Użycie: -p (szyfrowanie), -d (deszyfrowanie), -k (kryptoanaliza)")


if __name__ == "__main__":
    main()
