
import matplotlib.pyplot as plt
import numpy as np
import math

# set = np.arange(-4,4,0.1)
#
# cos_line = np.cos(set*math.pi/2)
# sin_line = np.sin(set)
# plt.plot(set, sin_line, 'r*', label='y=sin(x)')
# plt.plot(set, cos_line, 'b*', label='y=cos(x)')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()

math_set = np.arange(-10,10,0.1)


y = map(lambda x:math.sin(x) if x>0 else math.cos(x),math_set)

plt.plot(math_set, list(y))


