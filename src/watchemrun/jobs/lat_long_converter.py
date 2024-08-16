from dataclasses import dataclass
from watchemrun.schema.registry import ureg, Quantity
from watchemrun.consts.constants import chicago_cos_phi0
from typing import Tuple
import numpy as np


@dataclass
class LatLongConverter:
    radius_earth: Quantity = 3_958.8 * ureg("mile")

    def convert_to_xy(self, lat: float, long: float) -> Tuple[Quantity, Quantity]:
        return (self.radius_earth * long * chicago_cos_phi0, self.radius_earth * lat)


if __name__ == "__main__":
    test = LatLongConverter()
    print(test.convert_to_xy(lat=41 * np.pi / 180, long=45 * np.pi / 180))
