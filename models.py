import json
from typing import List

class Trainer:

    def __init__(self, data) -> None:
        pass


class TimeTable:

    def __init__(self, data) -> None:
        pass


class Bot:

    path = '' # path of source code, depends of Debug version

    def __init__(self, _path) -> None:
        self.path = _path

    def get_trainers(self) -> List[Trainer]:
        # Get data
        # To Do: Moved to DB
        with open(f'{self.path}trainers.json',"r", encoding="utf-8") as file:
            trainers = json.load(file)

        return [Trainer(data) for data in trainers]
