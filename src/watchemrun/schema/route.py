from pydantic import BaseModel, ConfigDict
from io import FileIO
from typing import List, Tuple
import gpxpy
from watchemrun.jobs.lat_long_converter import LatLongConverter
from pint import Quantity
import numpy as np


class RacePath(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    points: List[np.ndarray[Quantity]]

    @classmethod
    def from_gpx(cls, in_gpx_file: FileIO):
        gpx_object = gpxpy.parse(in_gpx_file)

        if len(gpx_object.tracks) > 1:
            raise ValueError("More than one track not implemented.")
        if len(gpx_object.tracks[0].segments) > 1:
            raise ValueError("More than one segment not implemented.")
        segments = gpx_object.tracks[0].segments[0].points

        convert = LatLongConverter()

        return cls(
            points=list(
                map(
                    lambda x: np.array(
                        convert.convert_to_xy(
                            x.latitude * np.pi / 180,
                            x.longitude * np.pi / 180,
                            dtype=Quantity,
                        )
                    ),
                    segments,
                )
            )
        )


class Route(BaseModel):

    path: RacePath
    length: float


if __name__ == "__main__":
    gpx_file = open(
        "/Users/johnwhitman/Projects/WatchEmRun/src/data/chicago_marathon.gpx", "r"
    )
    chicago_race = RacePath.from_gpx(gpx_file)

    total_length = 0

    for pointIndex, point in enumerate(chicago_race.points):
        if pointIndex == len(chicago_race.points) - 1:
            break
        first_point = np.array(point, dtype=Quantity)
        second_point = np.array(chicago_race.points[pointIndex + 1], dtype=Quantity)
        total_length += np.linalg.norm(first_point - second_point)
    print(total_length)
