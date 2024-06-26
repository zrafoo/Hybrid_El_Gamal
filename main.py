import random
from hashlib import sha256

# Определяем параметры
p = 97  # Простое число
a = 2
b = 3

def check_ab(a, b):
    if (4 * a ** 3 + 27 * b ** 2) % p == 0:
        return 'Wrong a,b'
    return True

# Определяем простое число q, делящее порядок группы точек эллиптической кривой
q = 5

# Определяем точки P,S на эллиптической кривой
P = (3, 6)
S=(3,6)

m = 512  # значение m, такое что p < m < 2p^2
r = 31

# Определяем отображения f и h
def f(x, y):
    return x % m
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def h(x, y, z):
    return y % m

# Определяем отображение mac
def mac(key, message):
    return int(sha256((str(key) + message).encode()).hexdigest(), 16) % r

# Функция выработки ключа kdf
def kdf(x, P):
    return int(sha256((str(x) + str(P)).encode()).hexdigest(), 16) % q

# Реализация эллиптической кривой и умножения точки
class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, x, y):
        return (y ** 2 - (x ** 3 + self.a * x + self.b)) % self.p == 0

    def point_addition(self, P, Q):
        if P == (None, None):
            return Q
        if Q == (None, None):
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y1 == -y2 % self.p:
            return (None, None)

        if P == Q:
            m = (3 * x1 ** 2 + self.a) * pow(2 * y1, -1, self.p)
        else:
            m = (y2 - y1) * pow(x2 - x1, -1, self.p)

        m = m % self.p

        x3 = (m ** 2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def scalar_multiplication(self, k, P):
        result = (None, None)
        addend = P

        for _ in range(k):
            result = self.point_addition(result, addend)

        return result

# Инициализация эллиптической кривой
curve = EllipticCurve(a, b, p) # Порядок 100

def generate_keys(curve,P):
    d=random.randint(1,q)
    bigY=EllipticCurve.scalar_multiplication(curve,d,P)
    return d,bigY

# Шифрование
def encrypt(message,p, P, k,U, m,S):
    xu,yu=U
    xs,ys=S
    alpha = (yu-ys)/(xu-xs) % p
    beta = (ys*xu-xs*yu)/(xu-xs) % p
    print('encrypt alpha beta', alpha, beta)

    W = curve.scalar_multiplication(k, P)
    print('W=',W)

    t = (f(alpha, yu) * message + h(alpha, beta, yu)) % m

    return t, W

# Расшифрование
def decrypt(curve,t, W, P, k, m,d,S,p):
    xw,yw=W
    if not EllipticCurve.is_on_curve(curve,xw,yw):
        return 'Не принимается'

    xu,yu= curve.scalar_multiplication(d, W)
    # Знает xu,yu и xs,ys, так что просто
    xs,ys=S
    alpha = (yu-ys)/(xu-xs) % p
    beta = (ys*xu-xs*yu)/(xu-xs) % p
    print('decrypt alpha beta',alpha,beta)

    # Вычисляем исходное сообщение
    s = (t - h(alpha,beta,yu))*gcd(f(alpha,yu),m) % m
    print(t,h(alpha,beta,yu),gcd(f(alpha,yu),m))
    return s

# Пример использования
message = 100
k = random.randint(1, q-1)
print('q=',q,'k=',k)

d,bigY=generate_keys(curve,P)
print('d=',d,'Y=',bigY)

U = curve.scalar_multiplication(k, bigY)
print('U=',U)

ciphertext, W = encrypt(message,p, P, k,U, m,S)
plaintext = decrypt(curve,ciphertext, W, P, k, m,d,S,p)

print("Сообщение:", message)
print("Зашифрованное сообщение:", ciphertext)
print("Расшифрованное сообщение:", plaintext)
