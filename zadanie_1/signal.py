import numpy as np
import math


class Signal:
    ##########################
    # CONSTANT
    ##########################
    _UNIT_NOISE_DISTRIBUTION = "UNIT_NOISE_DISTRIBUTION"  # S1
    _GAUSSIAN_NOISE = "GAUSSIAN_NOISE"
    _SINUSOIDAL_NOISE = "SINUSOIDAL_NOISE"
    _ONE_HALF_RECTIFIED_SINUSOIDAL_SIGNAL = "ONE_HALF_RECTIFIED_SINUSOIDAL_SIGNAL"
    _TWO_HALF_RECTIFIED_SINUSOIDAL_SIGNAL = "TWO_HALF_RECTIFIED_SINUSOIDAL_SIGNAL"
    _SQUARE_WAVE_SIGNAL = "SQUARE_WAVE_SIGNAL"
    _SYMMETRICAL_SQUARE_WAVE_SIGNAL = "SYMMETRICAL_SQUARE_WAVE_SIGNAL"
    _TRIANGULAR_SIGNAL = "TRIANGULAR_SIGNAL"
    _UNIT_JUMP = "UNIT_JUMP"
    _UNIT_IMPULSE = "UNIT_IMPULSE"
    _IMPULSE_NOISE = "IMPULSE_NOISE"

    def __init__(self):
        self.all_signals = self._generate_dict_with_all_signals()

    def _generate_dict_with_all_signals(self) -> dict:
        return {"UNIT_NOISE_DISTRIBUTION": self._unit_noise_distribution,
                "GAUSSIAN_NOISE": self._gaussian_noise,
                "SINUSOIDAL_NOISE": self._sinusoidal_noise,
                "ONE_HALF_RECTIFIED_SINUSOIDAL_SIGNAL": self._one_half_rectified_sinusoidal_signal,
                "TWO_HALF_RECTIFIED_SINUSOIDAL_SIGNAL": self._two_half_rectified_sinusoidal_signal,
                "SQUARE_WAVE_SIGNAL": self._square_wave_signal,
                "SYMMETRICAL_SQUARE_WAVE_SIGNAL": self._symmetrical_square_wave_signal,
                "TRIANGULAR_SIGNAL": self._triangular_signal,
                "UNIT_JUMP": self._unit_jump,
                "UNIT_IMPULSE": self._unit_impulse,
                "IMPULSE_NOISE": self._impulse_noise}

    def _unit_noise_distribution(self, A, t1, d) -> np.array:
        noise = np.array([np.random.uniform(low=-A, high=A, size=None) for _ in range(t1, d)])
        return noise

    def _gaussian_noise(self, A, t1, d) -> np.array:
        noise = np.array([(1/math.sqrt(2*math.pi)) * pow(math.e, (-pow(np.random.uniform(low=-A, high=A, size=None), 2)) / 2) for _ in range(t1, d)])
        return noise

    def _sinusoidal_noise(self):
        pass

    def _one_half_rectified_sinusoidal_signal(self):
        pass

    def _two_half_rectified_sinusoidal_signal(self):
        pass

    def _square_wave_signal(self):
        pass

    def _symmetrical_square_wave_signal(self):
        pass

    def _triangular_signal(self):
        pass

    def _unit_jump(self):
        pass

    def _unit_impulse(self):
        pass

    def _impulse_noise(self):
        pass

    def generate(self, signal: str):
        return self.all_signals[signal]()