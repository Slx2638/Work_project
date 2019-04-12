import numpy as np

people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
y_pos = np.arange(24)
print(y_pos)
total_width, n = 0.8, 2
width = total_width / n
y_pos=y_pos - (total_width - width) / 2
performance = 3 + 10 * np.random.rand(24)
print(y_pos)
print(performance)
