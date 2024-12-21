from .iloc import IlocDict
from .ploc import PlocDict

class SpecialHashMap(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def toSortedSet(self):
        return dict(sorted(self.items()))

    @property
    def iloc(self):
        return IlocDict(self)

    @property
    def ploc(self):
        return PlocDict(self)