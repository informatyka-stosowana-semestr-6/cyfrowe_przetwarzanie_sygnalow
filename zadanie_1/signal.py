import numpy as np
from numpy import random
import math
import statistics
import json


class Signal:

    def __init__(self):
        self.name = None
        self.all_signals = self._generate_dict_with_all_signals()
        self.MATH = self._generate_math()
        self.x_values = None
        self.y_values = None
        self.A = None
        self.T = None
        self.t1 = None
        self.d = None
        self.kw = None
        self.jump_time = None
        self.possibility = None
        self.freq = 60

        self.average = None
        self.absolut_average = None
        self.power_average = None
        self.variance = None
        self.effective_value = None


    def set_x(self):
        self.x_values = np.linspace(float(self.t1), float(self.t1) + float(self.d), int(float(self.d) * float(self.freq)))

    def _generate_dict_with_all_signals(self) -> dict:
        return {"UNIT_NOISE_DISTRIBUTION": self._unit_noise_distribution,
                "GAUSSIAN_NOISE": self._gaussian_noise,
                "SINUSOIDAL_SIGNAL": self._sinusoidal_signal,
                "ONE_HALF_RECTIFIED_SINUSOIDAL_SIGNAL": self._one_half_rectified_sinusoidal_signal,
                "TWO_HALF_RECTIFIED_SINUSOIDAL_SIGNAL": self._two_half_rectified_sinusoidal_signal,
                "SQUARE_WAVE_SIGNAL": self._square_wave_signal,
                "SYMMETRICAL_SQUARE_WAVE_SIGNAL": self._symmetrical_square_wave_signal,
                "TRIANGULAR_SIGNAL": self._triangular_signal,
                "UNIT_JUMP": self._unit_jump,
                "UNIT_IMPULSE": self._unit_impulse,
                "IMPULSE_NOISE": self._impulse_noise,
                "FROM_FILE": self.load}

    def _generate_math(self):
        return {"Dodawanie": self.add, "Odejmowanie": self.subtraction, "Mnożenie": self.multiply, "Dzielenie": self.division}

    def _unit_noise_distribution(self) -> np.array:
        self.y_values = np.array((random.uniform(-self.A, self.A, size=(len(self.x_values),))).tolist())

    def _gaussian_noise(self) -> np.array:
        self.y_values = np.array((random.normal(scale=self.A, size=(len(self.x_values),))).tolist())

    def _sinusoidal_signal(self):
        self.y_values = self.A * np.sin((2 * np.pi / self.T) * (self.x_values - self.t1))

    def _one_half_rectified_sinusoidal_signal(self):
        self.y_values = 0.5 * self.A * (np.sin((2 * np.pi / self.T) * (self.x_values - self.t1)) + np.abs(np.sin((2 * np.pi / self.T) * (self.x_values - self.t1))))

    def _two_half_rectified_sinusoidal_signal(self):
        self.y_values = self.A * np.abs(np.sin((2 * np.pi / self.T) * (self.x_values - self.t1)))

    def _square_wave_signal(self):
        values = []
        for x in self.x_values:
            if (((x - self.t1) % self.T) / self.T) < self.kw:
                values.append(self.A)
            else:
                values.append(0)
        self.y_values = values

    def _symmetrical_square_wave_signal(self):
        values = []
        for x in self.x_values:
            if (((x - self.t1) % self.T) / self.T) < self.kw:
                values.append(self.A)
            else:
                values.append(-self.A)
        self.y_values = values

    def _triangular_signal(self):
        values = []
        for x in self.x_values:
            if (((x - self.t1) % self.T) / self.T) < self.kw:
                values.append((self.A / (self.kw * self.T)) * ((x - self.t1) % self.T))
            else:
                values.append((-self.A / (self.T * (1 - self.kw)) * ((x - self.t1) % self.T)) + self.A / (1 - self.kw))
        self.y_values = values

        # alpha = (self.A) / (self.d / 2)
        # self.y_values = -self.A / 2 + self.A * ((self.x_values - 1/self.T) % self.d == self.d / 2) + alpha * \
        #        ((self.x_values - 1/self.T) % (self.d / 2)) * ((self.x_values - 1/self.T) % self.d <= self.d / 2) \
        #        + (self.A - alpha * ((self.x_values - 1/self.T) % (self.d / 2))) * ((self.x_values - 1/self.T) % self.d > self.d / 2)

    def _unit_jump(self):
        values = []
        for x in self.x_values:
            if x < self.jump_time:
                values.append(0)
            elif x == self.jump_time:
                values.append(0.5 * self.A)
            else:
                values.append(self.A)
        self.y_values = values

    def _unit_impulse(self):
        values = []
        for i in range(self.x_values.size - 1):
            if self.x_values[i] <= self.jump_time < self.x_values[i + 1]:
                values.append(self.A)
            else:
                values.append(0)
        values.append(0)
        self.y_values = values

    def _impulse_noise(self):
        values = []
        for x in self.x_values:
            if random.uniform(0, 1) < self.possibility:
                values.append(self.A)
            else:
                values.append(0)
        self.y_values = values

    def add(self, s1, s2):
        values = []
        for i in range(s1.x_values.size):
            values.append(s1.y_values[i] + s2.y_values[i])
        self.x_values = s1.x_values
        self.y_values = values

    def subtraction(self, s1, s2):
        values = []
        for i in range(s1.x_values.size):
            values.append(s1.y_values[i] - s2.y_values[i])
        self.x_values = s1.x_values
        self.y_values = values

    def multiply(self, s1, s2):
        values = []
        for i in range(s1.x_values.size):
            values.append(s1.y_values[i] * s2.y_values[i])
        self.x_values = s1.x_values
        self.y_values = values

    def division(self, s1, s2):
        values = []
        for i in range(s1.x_values.size):
            values.append(s1.y_values[i] / s2.y_values[i])
        self.x_values = s1.x_values
        self.y_values = values

    def generate(self, signal: str):
        self.set_x()
        self.all_signals[signal]()

    def save_to_file(self, file_name, signal):
        with open(file_name, "w") as file:
            file.write(f"signal = {signal}")
            file.write(f"x = {self.x_values}")
            file.write(f"y = {self.y_values}")

    def load(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        self.name = data["signal name"]
        self.t1 = data["t1"]
        self.A = data["A"]
        self.freq = data["freq"]
        self.x_values = np.array(data["x_values"])
        self.y_values = np.array(data["y_values"])
        self.d = data["d"]
        self.T = data["T"]
        self.kw = data["kw"]
        self.jump_time = data["jump_time"]
        self.possibility = data["possibility"]

    # Statistics
    def _calculate_avg(self):
        self.average = statistics.mean(self.y_values)

    def _calculate_abs_avg(self):
        self.absolut_average = abs(self.average)

    def _calculate_power_avg(self):
        if self.T == 0:
            tmp = np.power(self.y_values, 2)
            self.power_average = np.around(np.nanmean(tmp), 4)
        else:
            rest = self.d % self.T * self.freq
            y_temp = self.y_values[0:int(len(self.y_values) - rest)]
            tmp = np.power(y_temp, 2)
            self.power_average = np.around(np.nanmean(tmp), 4)

    def _calculate_variance(self):
        if self.T == 0:
            self.variance = np.around(np.nanvar(self.y_values), 4)
        else:
            rest = self.d % self.T * self.freq
            y_temp = self.y_values[0:int(len(self.y_values) - rest)]
            self.variance = np.around(np.nanvar(y_temp), 4)

    def _calculate_effective_value(self):
        self.effective_value = np.around(np.sqrt(self.power_average), 4)

    def calculate_all_statistics(self):
        self._calculate_avg()
        self._calculate_abs_avg()
        self._calculate_power_avg()
        self._calculate_variance()
        self._calculate_effective_value()
