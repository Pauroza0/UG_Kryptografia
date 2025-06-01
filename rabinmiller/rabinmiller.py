#Paulina Rozanska

import sys
import random
import math


def fermat_test(n, tries=40):
    if n == 2 or n == 3:
        return True, None
    if n < 2 or n % 2 == 0:
        return False, 2
    for _ in range(tries):
        a = random.randrange(2, n-1)
        d = math.gcd(a, n)
        if d > 1:
            return False, d
        if pow(a, n-1, n) != 1:
            return False, None
    return True, None


def miller_rabin(n, r=None, tries=20):
    if n == 2 or n == 3:
        return True, None
    if n < 2 or n % 2 == 0:
        return False, 2

    if r is None:
        r = n - 1
    k = 0
    m = r
    while m % 2 == 0:
        m //= 2
        k += 1

    for _ in range(tries):
        a = random.randrange(2, n - 1)
        d = math.gcd(a, n)
        if d != 1:
            return True, d

    def check(a):
        g = math.gcd(a, n)
        if 1 < g < n:
            return False, g
        b = pow(a, m, n)
        if b == 1 or b == n - 1:
            return True, None
        for _ in range(k - 1):
            b = pow(b, 2, n)
            if b == n - 1:
                return True, None
        dzielnik = math.gcd(b - 1, n)
        if 1 < dzielnik < n:
            return False, dzielnik
        return False, None

    if r:
        result, dzielnik = check(r)
        return result, dzielnik

    for _ in range(tries):
        a = random.randrange(2, n - 1)
        result, dzielnik = check(a)
        if not result:
            return False, dzielnik
    return True, None


def main():
    use_fermat = '-f' in sys.argv
    in_file = 'wejscie.txt'
    out_file = 'wyjscie.txt'


    with open(in_file) as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    witness = None
    if not use_fermat:
        if len(lines) == 2:
            witness = int(lines[1])
        elif len(lines) == 3:
            witness = int(lines[1]) * int(lines[2]) - 1

    with open(out_file, 'w', encoding='utf-8') as f:
        if use_fermat:
            wynik = fermat_test(n)
            if wynik:
                f.write("prawdopodobnie pierwsza\n")
            else:
                f.write("na pewno złożona\n")
        else:
            if witness:
                wynik, dzielnik = miller_rabin(n, witness)
                if dzielnik:
                    f.write(f"{dzielnik}\n")
                elif wynik:
                    f.write("prawdopodobnie pierwsza\n")
                else:
                    f.write("na pewno złożona\n")
            else:
                wynik, dzielnik = miller_rabin(n)
                if dzielnik:
                    f.write(f"{dzielnik}\n")
                elif wynik:
                    f.write("prawdopodobnie pierwsza\n")
                else:
                    f.write("na pewno złożona\n")


if __name__ == '__main__':
    main()
