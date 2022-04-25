from zadanie_1.signal import Signal
import matplotlib.pyplot as plt
s = Signal()

plt.plot(s._gaussian_noise(10, 0, 100))
plt.show()

