from dataclasses import dataclass


class TargetValueMapping:
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1

    def _asdict(self):
        return self.__dict__

    def reverse_mapping(self):
        mappingResponse = self._asdict()
        return dict(zip(mappingResponse.values(), mappingResponse.keys()))
