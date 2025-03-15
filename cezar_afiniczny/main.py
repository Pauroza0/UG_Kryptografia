##Paulina Różańska

import sys


def usun_polskie_znaki(text):
    zamiana = {
        'ą': 'a', 'ć': 'c', 'ę': 'e',
        'ł': 'l', 'ń': 'n', 'ó': 'o',
        'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E',
        'Ł': 'L', 'Ń': 'N', 'Ó': 'O',
        'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    return ''.join(zamiana.get(znak, znak) for znak in text)


def cezar_encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + key) % 26 + offset)
        else:
            result += char
    return result


def cezar_decrypt(text, key):
    return cezar_encrypt(text, -key)


def odwrotnosc_modulo(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def affiniczny_encrypt(text, a, b):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr(((a * (ord(char) - offset) + b) % 26) + offset)
        else:
            result += char
    return result


def affiniczny_decrypt(text, a, b):
    result = ""
    odwrotnosc = odwrotnosc_modulo(a)
    if odwrotnosc is None:
        raise ValueError("Brak odwrotnosci modulo dla podanego klucza a")
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((odwrotnosc * (ord(char) - offset - b)) % 26 + offset)
        else:
            result += char
    return result


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)


def kryptoanaliza_cezar_jawny(helptext, crypt):
    for key in range(1, 26):
        if cezar_encrypt(helptext, key) == crypt[:len(helptext)]:
            write_file("foundkey.txt", str(key))
            return key
    return None


def kryptoanaliza_cezar_niejawny(crypt):
    wynik = []
    for key in range(1, 26):
        decoded = cezar_decrypt(crypt, key)
        wynik.append(f"key={key}: {decoded}")
    return '\n'.join(wynik)


def kryptoanaliza_afiniczny_jawny(helptext, crypt):
    for a in [x for x in range(1, 26) if odwrotnosc_modulo(x) is not None]:
        for b in range(26):
            if affiniczny_encrypt(helptext, a, b) == crypt[:len(helptext)]:
                write_file("foundkey.txt", f"{a} {b}")
                return a, b
    return None


def kryptoanaliza_afiniczny_niejawny(crypt):
    wynik = []
    for a in [x for x in range(1, 26) if odwrotnosc_modulo(x)]:
        odwrotnosc = odwrotnosc_modulo(a)
        for b in range(26):
            decoded = affiniczny_encrypt(crypt, odwrotnosc, -b * odwrotnosc)
            wynik.append(f"a={a}, b={b}:\n{decoded}\n")
    return '\n'.join(wynik)


def check_key_cezar():
    key = int(read_file('key.txt').split()[0])
    if 1 > key > 25:
        raise ValueError("Nieprawidlowy klucz dla szyfru Cezara")
    return key


def check_key_afiniczny():
    key = read_file('key.txt').split()
    a, b = int(key[0]), int(key[1])
    if odwrotnosc_modulo(a) is None:
        raise ValueError("Nieprawidlowy klucz dla szyfru afiniczniego")
    return a, b


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Nieprawidlowa ilosc argumetentow")
        sys.exit(1)

    szyfr, operacja = sys.argv[1], sys.argv[2]

    try:
        if szyfr == '-c':

            if operacja == '-e':
                key = check_key_cezar()
                text = usun_polskie_znaki(read_file("plain.txt"))
                encrypted = cezar_encrypt(text, key)
                write_file("crypt.txt", encrypted)

            elif operacja == '-d':
                key = check_key_cezar()
                text = read_file("crypt.txt")
                decrypted = cezar_decrypt(text, key)
                write_file("decrypt.txt", decrypted)

            elif operacja == '-j':
                helptext = usun_polskie_znaki(read_file("extra.txt"))
                crypt = read_file("crypt.txt")
                key_found = kryptoanaliza_cezar_jawny(helptext, crypt)
                if key_found is None:
                    print("Nie znaleziono klucza")
                    sys.exit(1)
                decrypted = cezar_decrypt(crypt, key_found)
                write_file("decrypt.txt", decrypted)

            elif operacja == '-k':
                crypt = read_file("crypt.txt")
                wynik = kryptoanaliza_cezar_niejawny(crypt)
                write_file("decrypt.txt", wynik)
            else:
                print("Nie prawidlowa operacja")
                sys.exit(1)

        elif szyfr == '-d':

            if operacja == '-e':
                a, b = check_key_afiniczny()
                text = usun_polskie_znaki(read_file("plain.txt"))
                encrypted = affiniczny_encrypt(text, a, b)
                write_file("crypt.txt", encrypted)

            elif operacja == '-d':
                a, b = check_key_afiniczny()
                text = read_file("crypt.txt")
                decrypted = affiniczny_decrypt(text, a, b)
                write_file("decrypt.txt", decrypted)
            elif operacja == '-j':
                crypt = read_file("crypt.txt")
                helptext = read_file("extra.txt")
                key = kryptoanaliza_afiniczny_jawny(helptext, crypt)
                if key:
                    decrypted = affiniczny_decrypt(crypt, key[0], key[1])
                    write_file("decrypt.txt", decrypted)
                else:
                    print("Nieznaleziono klucza")

            elif operacja == '-k':
                crypt = read_file("crypt.txt")
                wynik = kryptoanaliza_afiniczny_niejawny(crypt)
                write_file('decrypt.txt', wynik)
        else:
            print("Nieprawidłowy typ szyfru")
            sys.exit(1)

    except Exception as e:
        print("Błąd:", e)
        sys.exit(1)
