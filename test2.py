import math
# from scipy import misc
a = 2.5
# f = lambda dx: (58**a - dx**a)**(1/a)
# g = lambda dx: (42**a - dx**a)**(1/a)
# d = lambda func, a: round(math.degrees(math.atan(misc.derivative(func, a))), 2)
# angle = round(math.degrees(f(0)))

f = lambda dx: 5*dx**2 * (-dx**(1/2)*dx**2 + 3364 * 58**(1/2))**(1/a) / (5*dx**3 - 16820 * 58**(1/2) * dx**(1/2))
f2 = lambda dx: 5*(-dx)**2 * (-(-dx)**(1/2)*(-dx)**2 + 3364 * 58**(1/2))**(1/a) / (5*(-dx)**3 - 16820 * 58**(1/2) * (-dx)**(1/2))
d = lambda func, a: round(math.degrees(math.atan(func(a))), 2)
pass