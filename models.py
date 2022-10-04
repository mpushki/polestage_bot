import json
from typing import List

class Trainer:

    __slots__ = (
        'id'
        'name',
        'inst',
        'types',
        'image',
        'description'
        )

    def __init__(self, id, data) -> None:
        self.id = id
        self.name = data['name']
        self.inst = data['inst']
        self.types = data['types']
        self.image = data['image']
        self.description = data['description']

    @property
    def image_path(self, path):
        return f'{path}assets/{self.image}.jpg'


class TimeTable:

    __slot__ = ('day', 'schedule')

    def __init__(self, day, data) -> None:
        self.day = day
        self.schedule = data

class Bot:

    path = '' # path of source code, depends of Debug version

    def __init__(self, _path) -> None:
        self.path = _path

    def get_trainers(self) -> List[Trainer]:
        # Get data
        # To Do: Moved to DB
        with open(f'{self.path}trainers.json',"r", encoding="utf-8") as file:
            trainers = json.load(file)

        return [Trainer(key, value) for (key, value) in trainers]
