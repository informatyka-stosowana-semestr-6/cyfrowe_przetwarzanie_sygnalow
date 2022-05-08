import numpy as np
from numpy import random, sin

SIGNALS = [
    "S1 - szum o rozkladzie jednostajnym",
    "S2 - szum gaussawski",
    "S3 - sygnal sinusoidalny",
    "S4 - sygnal sinusoidalny wyprostowany jednopolowkowo",
    "S5 - sygnal sinusoidalny wyprostowany dwupolowkowo",
    "S6 - sygnal prostokatny",
    "S7 - sygnal prostokatny symetryczny",
    "S8 - sygnal trojkatny",
    "S9 - skok jednostkowy",
    "S10 - impuls jednostkowy",
    "S11 - szum impulsowy"
]


class Signal:
    signal_type = ""
    discrete = False
    amplitude = 10
    start_time = 0
    signal_duration = 1
    base_period = 0
    fill_factor = 0.0
    jump_time = 5.0
    jump_prob = 0.3
    freq = 60
    x_values = []
    y_values = []
    avg = 0.0
    avg_bezwzgl = 0.0
    moc_srednia = 0.0
    wariancja = 0.0
    wart_skuteczna = 0.0

    def __init__(self, signal_type, freq, params) -> None:
        super().__init__()
        self.signal_type = signal_type
        self.freq = int(freq)
        if "S" in signal_type:
            self.amplitude = float(params[0])
            self.start_time = float(params[1])
            self.signal_duration = float(params[2])
            self.base_period = float(params[3])
            self.fill_factor = float(params[4])
            self.jump_time = float(params[5])
            self.jump_prob = float(params[6])
        if "S10" in signal_type or "S11" in signal_type:
            self.discrete = True

    def generate_signal(self):
        self.x_values = x = np.linspace(float(self.start_time), float(self.start_time) + float(self.signal_duration),
                                        int(float(self.signal_duration) * self.freq))
        self.y_values = {
            "S1 - szum o rozkladzie jednostajnym":
                self.S1,
            "S2 - szum gaussawski":
                self.S2,
            "S3 - sygnal sinusoidalny":
                self.S3,
            "S4 - sygnal sinusoidalny wyprostowany jednopolowkowo":
                self.S4,
            "S5 - sygnal sinusoidalny wyprostowany dwupolowkowo":
                self.S5,
            "S6 - sygnal prostokatny":
                self.S6,
            "S7 - sygnal prostokatny symetryczny":
                self.S7,
            "S8 - sygnal trojkatny":
                self.S8,
            "S9 - skok jednostkowy":
                self.S9,
            "S10 - impuls jednostkowy":
                self.S10,
            "S11 - szum impulsowy":
                self.S11,
        }[self.signal_type](x)
        self.count_stats()

        return self.y_values

    def S1(self, items):
        return (random.uniform(-self.amplitude, self.amplitude, size=(len(items),))).tolist()

    def S2(self, items):
        return (random.normal(scale=self.amplitude, size=(len(items),))).tolist()

    def S3(self, items):
        return self.amplitude * sin((2 * np.pi / self.base_period) * (items - self.start_time))

    def S4(self, items):
        return 0.5 * self.amplitude * (np.sin((2 * np.pi / self.base_period) * (items - self.start_time)) +
                                       np.abs(np.sin((2 * np.pi / self.base_period) * (items - self.start_time))))

    def S5(self, items):
        return self.amplitude * np.abs(np.sin((2 * np.pi / self.base_period) * (items - self.start_time)))

    def S6(self, items):
        values = []
        for item in items:
            if (((item - self.start_time) % self.base_period) / self.base_period) < self.fill_factor:
                values.append(self.amplitude)
            else:
                values.append(0)
        return values

    def S7(self, items):
        values = []
        for item in items:
            if (((item - self.start_time) % self.base_period) / self.base_period) < self.fill_factor:
                values.append(self.amplitude)
            else:
                values.append(-self.amplitude)
        return values

    def S8(self, items):
        values = []
        for item in items:
            if (((item - self.start_time) % self.base_period) / self.base_period) < self.fill_factor:
                values.append((self.amplitude / (self.fill_factor * self.base_period)) *
                              ((item - self.start_time) % self.base_period))
            else:
                values.append((-self.amplitude / (self.base_period * (1 - self.fill_factor)) *
                               ((item - self.start_time) % self.base_period)) + self.amplitude / (1 - self.fill_factor))
        return values

    def S9(self, items):
        values = []
        for item in items:
            if item < self.jump_time:
                values.append(0)
            elif item == self.jump_time:
                values.append(0.5 * self.amplitude)
            else:
                values.append(self.amplitude)
        return values

    def S10(self, items):
        values = []
        for i in range(items.size - 1):
            if items[i] <= self.jump_time < items[i + 1]:
                values.append(self.amplitude)
            else:
                values.append(0)
        values.append(0)
        return values

    def S11(self, items):
        values = []
        for item in items:
            if random.uniform(0, 1) < self.jump_prob:
                values.append(self.amplitude)
            else:
                values.append(0)
        return values

    def dodaj(self, other):
        result = Signal("Obliczony", self.freq, [])
        values = []
        for i in range(self.x_values.size):
            values.append(self.y_values[i] + other.y_values[i])
        result.x_values = self.x_values
        result.y_values = values
        result.count_stats()
        return result

    def usun(self, other):
        result = Signal("Obliczony", self.freq, [])
        values = []
        for i in range(self.x_values.size):
            values.append(self.y_values[i] - other.y_values[i])
        result.x_values = self.x_values
        result.y_values = values
        result.count_stats()
        return result

    def mnozenie(self, other):
        result = Signal("Obliczony", self.freq, [])
        values = []
        for i in range(self.x_values.size):
            values.append(self.y_values[i] * other.y_values[i])
        result.x_values = self.x_values
        result.y_values = values
        result.count_stats()
        return result

    def dzielenie(self, other):
        result = Signal("Obliczony", self.freq, [])
        values = []
        for i in range(self.x_values.size):
            values.append(self.y_values[i] / other.y_values[i])
            print(self.y_values[i] / other.y_values[i])
        result.x_values = self.x_values
        result.y_values = values
        result.count_stats()
        return result

    def __str__(self) -> str:
        return "Start_time: " + str(self.start_time) + "\nFrequency: " + str(self.freq) + "\n" \
               + " ".join(str(y) for y in self.y_values)
    
    def count_stats(self):
        self.calc_srednia()
        self.calc_wariancja()
        self.calc_srednia_bezwzgledna()
        self.calc_moc_srednia()
        self.calc_wartosc_skuteczna()

    def calc_srednia(self):
        if self.base_period == 0:
            self.avg = np.around(np.nanmean(self.y_values), 4)
        else:
            rest = self.signal_duration % self.base_period * self.freq
            y_temp = self.y_values[0:int(len(self.y_values)-rest)]
            self.avg = np.around(np.nanmean(y_temp), 4)
        return self.avg

    def calc_srednia_bezwzgledna(self):
        if self.base_period == 0:
            tmp = np.abs(self.y_values)
            self.avg_bezwzgl = np.around(np.nanmean(tmp), 4)
        else:
            rest = self.signal_duration % self.base_period * self.freq
            y_temp = self.y_values[0:int(len(self.y_values)-rest)]
            tmp = np.abs(y_temp)
            self.avg_bezwzgl = np.around(np.nanmean(tmp), 4)
        return self.avg_bezwzgl

    def calc_moc_srednia(self):
        if self.base_period == 0:
            tmp = np.power(self.y_values, 2)
            self.moc_srednia = np.around(np.nanmean(tmp), 4)
        else:
            rest = self.signal_duration % self.base_period * self.freq
            y_temp = self.y_values[0:int(len(self.y_values) - rest)]
            tmp = np.power(y_temp, 2)
            self.moc_srednia = np.around(np.nanmean(tmp), 4)
        return self.moc_srednia

    def calc_wariancja(self):
        if self.base_period == 0:
            self.wariancja = np.around(np.nanvar(self.y_values), 4)
        else:
            rest = self.signal_duration % self.base_period * self.freq
            y_temp = self.y_values[0:int(len(self.y_values) - rest)]
            self.wariancja = np.around(np.nanvar(y_temp), 4)
        return self.wariancja

    def calc_wartosc_skuteczna(self):
        self.wart_skuteczna = np.around(np.sqrt(self.moc_srednia), 4)
        return self.wart_skuteczna
