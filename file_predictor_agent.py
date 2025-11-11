from predictor_agent import Predictor_Agent
import json
import os


class File_Predictor_Agent(Predictor_Agent):

    def __init__(self, filename: str):
        file = open(filename)
        obj = json.load(file)
        self.prediction_dict = {}
        for prediction in obj:
            self.prediction_dict[prediction[0]] = prediction[1]
        file.close()

    def predict_image(self, image_path: str) -> str:
        image_name = os.path.basename(image_path)
        if image_name not in self.prediction_dict:
            raise ValueError(image_name + " not found")
        return self.prediction_dict[image_name]
