from abc import ABC, abstractmethod
import json


class Predictor_Agent(ABC):
    _label_set_initialized: bool = False
    label_set: list[str] = []

    @abstractmethod
    def predict_image(self, image_path: str) -> str:
        pass

    @classmethod
    def initialize_label_set(cls, filename):
        if cls._label_set_initialized:
            return
        file = open(filename)
        dataset = json.load(file)
        label_dict = {}
        for datum in dataset:
            if datum[1] not in label_dict:
                label_dict[datum[1]] = True
        cls.label_set = list(label_dict.keys())
        cls._label_set_initialized = True


Predictor_Agent.initialize_label_set("./assets/preprocessed_dataset.json")
