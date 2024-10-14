import random
from abc import ABC, abstractmethod


class DamageCalculator(ABC):
    @abstractmethod
    def calculate(self, difficulty) -> int:
        pass


class DefaultDamageCalculator(DamageCalculator):
    def calculate(self, difficulty) -> int:
        return random.randint(difficulty, difficulty + 10)
