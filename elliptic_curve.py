from sympy import mod_inverse, isprime

# Параметры эллиптической кривой
p = 97
a = 2
b = 3
# Порядок подгруппы
order = 5
# Функция для вычисления правой части уравнения эллиптической кривой
def elliptic_curve(x):
    return (x**3 + a*x + b) % p

# Функция для проверки, является ли число квадратичным вычетом по модулю p
def is_quadratic_residue(n, p):
    return pow(n, (p - 1) // 2, p) == 1

# Поиск всех точек на эллиптической кривой
points = []
for x in range(p):
    y_squared = elliptic_curve(x)
    if is_quadratic_residue(y_squared, p):
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))

# Функция для добавления двух точек на эллиптической кривой
def add_points(P, Q, p):
    if P == Q:
        if P[1] == 0:
            return None  # Точка на бесконечности
        l = (3 * P[0]**2 + a) * mod_inverse(2 * P[1], p) % p
    else:
        if P[0] == Q[0]:
            return None  # Точка на бесконечности
        l = (Q[1] - P[1]) * mod_inverse(Q[0] - P[0], p) % p
    x = (l**2 - P[0] - Q[0]) % p
    y = (l * (P[0] - x) - P[1]) % p
    return (x, y)

# Функция для умножения точки на скаляр
def multiply_point(P, k, p):
    Q = P
    R = None
    while k > 0:
        if k % 2 == 1:
            if R is None:
                R = Q
            else:
                R = add_points(R, Q, p)
        Q = add_points(Q, Q, p)
        k //= 2
    return R

# Проверка порядка каждой точки
def find_point_with_order(points, order, p):
    for P in points:
        Q = multiply_point(P, order, p)
        if Q is None:
            return P
    return None


# Поиск точки, порождающей циклическую подгруппу заданного порядка
generating_point = find_point_with_order(points, order, p)
print("Точка, порождающая циклическую подгруппу порядка", order, ":", generating_point)
