import math
import random
from dataclasses import dataclass
from functools import cached_property

from utils import Log

log = Log('Angle')


@dataclass
class Angle:
    angle_deg: float

    @cached_property
    def rad(self):
        return math.pi * self.angle_deg / 180

    def __str__(self) -> str:
        return f'{self.angle_deg:.1f}°'

    def __repr__(self) -> str:
        return f'{self.angle_deg:.1f}°'

    def __add__(self, other: 'Angle') -> 'Angle':
        assert isinstance(other, Angle)
        return Angle(self.angle_deg + other.angle_deg)

    def __sub__(self, other: 'Angle') -> 'Angle':
        assert isinstance(other, Angle)
        return Angle(self.angle_deg - other.angle_deg)

    def __neg__(self) -> 'Angle':
        return Angle(-self.angle_deg)

    @staticmethod
    def random():
        return Angle(random.uniform(0, 360))
