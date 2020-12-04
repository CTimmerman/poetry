import posixpath

from collections import namedtuple
from enum import Enum
from pathlib import Path
from typing import List
from typing import NamedTuple

from .wheel import Wheel


class Scheme(Enum):

    PURELIB = "purelib"
    PLATLIB = "platlib"
    DATA = "data"
    SCRIPTS = "scripts"
    HEADERS = "headers"


Decision: NamedTuple[Path, Scheme] = namedtuple("Decision", ["path", "scheme"])


class SchemeDecisionMaker:
    def __init__(self, wheel: Wheel, root_scheme: Scheme) -> None:
        self._wheel = wheel
        self._data_name = wheel.data_name
        self._root_scheme = root_scheme

    def decide(self) -> List[Decision]:
        decisions = []
        for path in self._wheel.files:
            decisions.append(self.decide_for_path(path))

        return decisions

    def decide_for_path(self, path: Path) -> Decision:
        if not posixpath.commonprefix([self._data_name, path.as_posix()]):
            return Decision(path, self._root_scheme)

        left, right = posixpath.split(path)
        while left != self._data_name:
            left, right = posixpath.split(left)

        scheme_name = right
        # TODO: raise an error if scheme is invalid

        return Scheme.__members__[scheme_name]


class Installer:
    def __init__(self, name: str) -> None:
        self._name = name

    def install(self, wheel: Wheel, destination: Path) -> None:
        metadata = wheel.metadata

        # TODO: Check wheel format version
        root_scheme = Scheme.PURELIB
        if not metadata["Root-Is-Purelib"]:
            root_scheme = Scheme.PLATLIB

        decisions = self.get_decisions(wheel, root_scheme)

        for decision in decisions:
            pass

    def get_decisions(self, wheel: Wheel, root_scheme: Scheme) -> List[Decision]:
        decision_maker = SchemeDecisionMaker(wheel, root_scheme)

        return decision_maker.decide()
