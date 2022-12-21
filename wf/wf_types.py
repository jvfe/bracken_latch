from dataclasses import dataclass
from enum import Enum

from dataclasses_json import dataclass_json
from latch.types import LatchDir, LatchFile


@dataclass_json
@dataclass
class Sample:
    name: str
    data: LatchFile


@dataclass_json
@dataclass
class BrackenSample(Sample):
    database: LatchDir
    read_length: str
    classification_level: str
    threshold: int


class ReadLength(Enum):
    _50 = "50"
    _75 = "75"
    _100 = "100"
    _150 = "150"
    _200 = "200"
    _250 = "250"
    _300 = "300"


class ClassificationLevel(Enum):
    D = "D"
    P = "P"
    C = "C"
    O = "O"
    F = "F"
    G = "G"
    S = "S"
