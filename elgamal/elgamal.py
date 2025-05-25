##Paulina Różańska

import sys
import random
import math


def euklides_roz(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = euklides_roz(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):  # odwrotnosc mod
    g, x, y = euklides_roz(a, m)
    if g != 1:
        raise Exception('brak odwrotnosci')
    else:
        return x % m


def czy_pierwsza(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def wczytaj_p_g(filename):
    with open(filename) as f:
        p = int(f.readline().strip())
        g = int(f.readline().strip())
    return p, g


def generuj_klucz(p, g):
    b = random.randint(2, p - 2)
    beta = pow(g, b, p)
    return b, beta


def zapisz_klucz(p, g, key, filename):
    with open(filename, 'w') as f:
        f.write(f"{p}\n{g}\n{key}\n")


def wczytaj_klucz(filename):
    with open(filename) as f:
        p = int(f.readline())
        g = int(f.readline())
        beta = int(f.readline())
    return p, g, beta


def szyfruj(p, g, beta, m):
    k = random.randint(2, p - 2)
    r = pow(g, k, p)
    s = (m * pow(beta, k, p)) % p
    return r, s


def deszyfruj(p, b, r, s):
    rb = pow(r, b, p)
    rb_inv = modinv(rb, p)
    m = (s * rb_inv) % p
    return m


def podpisz(p, g, b, m):
    while True:
        k = random.randint(2, p - 2)
        if math.gcd(k, p - 1) == 1:
            break
    r = pow(g, k, p)
    k_inv = modinv(k, p - 1)  # odwrotnosc modularna k mod p - 1
    x = ((m - b * r) * k_inv) % (p - 1)
    return r, x


def weryfikuj_podpis(p, g, beta, m, r, x):
    left = pow(g, m, p)
    right = (pow(beta, r, p) * pow(r, x, p)) % p
    return left == right


def wczytaj_plik(filename):
    with open(filename) as f:
        return int(f.readline().strip())


def zapisz_wiadomosc(filename, m):
    with open(filename, 'w') as f:
        f.write(f'{m}\n')


def main():
    if len(sys.argv) < 2:
        print("use: python elgamal.py -opcja")
        sys.exit(1)

    opcja = sys.argv[1]

    if opcja == '-k':
        p, g = wczytaj_p_g('elgamal.txt')
        b, beta = generuj_klucz(p, g)
        zapisz_klucz(p, g, b, 'private.txt')
        zapisz_klucz(p, g, beta, 'public.txt')
    elif opcja == '-e':
        p, g, beta = wczytaj_klucz('public.txt')
        m = wczytaj_plik('plain.txt')
        if m >= p:
            print('Wiadomość za duża (m >= p)')
            sys.exit(2)
        r, s = szyfruj(p, g, beta, m)
        with open('crypto.txt', 'w') as f:
            f.write(f'{r}\n{s}\n')
    elif opcja == '-d':
        p, g, b = wczytaj_klucz('private.txt')
        with open('crypto.txt') as f:
            r = int(f.readline())
            s = int(f.readline())
        m = deszyfruj(p, b, r, s)
        zapisz_wiadomosc('decrypt.txt', m)
    elif opcja == '-s':
        p, g, b = wczytaj_klucz('private.txt')
        m = wczytaj_plik('message.txt')
        r, x = podpisz(p, g, b, m)
        with open('signature.txt', 'w') as f:
            f.write(f'{m}\n{r}\n{x}\n')
    elif opcja == '-v':
        p, g, beta = wczytaj_klucz('public.txt')
        with open('signature.txt') as f:
            m = int(f.readline())
            r = int(f.readline())
            x = int(f.readline())
        wynik = weryfikuj_podpis(p, g, beta, m, r, x)
        with open('verify.txt', 'w') as f:
            f.write('T\n' if wynik else 'N\n')
        print('T' if wynik else 'N')
    else:
        print('Nieznana opcja')


if __name__ == '__main__':
    main()
