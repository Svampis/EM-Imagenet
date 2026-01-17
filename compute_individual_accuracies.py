from file_predictor_agent import File_Predictor_Agent
import json
import numpy as np
from matplotlib import pyplot as plt
import time

np.set_printoptions(threshold=100000)
real_labels_file = open("./assets/preprocessed_dataset.json")

dataset = json.load(real_labels_file)

class_labels = File_Predictor_Agent.label_set.copy()

class_label_dict = {}
i = 0
for label in class_labels:
    class_label_dict[label] = i
    i += 1

predictor_a = File_Predictor_Agent("llm_classifications/gpt41nano_classifications.json")
predictor_b = File_Predictor_Agent("llm_classifications/gpt41mini_classifications.json")
predictor_c = File_Predictor_Agent("llm_classifications/grok2_classifications.json")
predictor_d = File_Predictor_Agent("llm_classifications/gpt4o_classifications.json")
predictors = [predictor_a, predictor_b, predictor_c, predictor_d]

accuracies = []
precisions = []
recalls = []
for predictor in predictors:
    correct = 0
    for datum in dataset:
        if predictor.predict_image(datum[0]) == datum[1]:
            correct += 1
    print(correct / len(dataset))
    
