import numpy as np
from matplotlib import pyplot

N = 10
ys = np.array([1,3,-5,3,5,6,7,8,20,-30], dtype=np.float64)
xs = np.array([1,2,3,4,5,6,7,8,9,10], dtype=np.float64)

trend = np.polyfit(xs, ys, 1)

pyplot.plot(xs, ys, 'o')
trendpoly = np.poly1d(trend)
pyplot.plot(xs, trendpoly(xs))

print(trendpoly)

pyplot.show()
