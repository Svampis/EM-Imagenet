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

predictions_matrix = []
for predictor in predictors:
    predictions = []
    for datum in dataset:
        predictions.append(class_label_dict[predictor.predict_image(datum[0])])
    predictions_matrix.append(predictions)

# We're going to start with 0.5 across the diagonal
# (Assuming 50% accuracy)
starting_confidence = 0.5
starting_confusion_matrix = np.full(
    (len(class_labels), len(class_labels)),
    (1 - starting_confidence) / (len(class_labels) - 1)
)

for i in range(len(class_labels)):
    starting_confusion_matrix[i][i] = starting_confidence

confusion_matrices = []
for i in range(len(predictors)):
    confusion_matrices.append(starting_confusion_matrix.copy())

# Metrics using ReaL labels as ground truth
accuracies: list[float] = []
precisions: list[float] = []
recalls: list[float] = []
real_prediction_dict = {}  # We'll use this to do those ground-truth comparions
for datum in dataset:
    real_prediction_dict[datum[0]] = datum[1]

start_time = time.time()
epochs = 40
for epoch in range(epochs):
    print("Epoch: " + str(epoch))

    # Generate heatmaps of the confusion matrices
    i = 1
    plt.figure()
    for confusion_matrix in confusion_matrices:
        fig, ax = plt.subplots()
        ax.imshow(confusion_matrix)
        plt.savefig(
            "./results/confusion_matrix_heatmaps/heatmap" + str(i) + "_" + str(epoch).zfill(4) + ".png",
            dpi=300,
            bbox_inches="tight"
        )
        i += 1

    # Release memory allocated to create confusion matrix heatmaps
    plt.close()

    # E step: compute a n x K matrix M
    # where n is the number of data points
    # where K is the number of classes
    # where M[i,j] is the probability data point i belongs to class j
    M = np.zeros((len(dataset), len(class_labels)))

    i = 0
    for i in range(len(dataset)):
        datum = dataset[i][0]
        predictions = [
            predictor[i]
            for predictor in predictions_matrix
        ]
        for j in range(len(class_labels)):
            likelihood_of_label = 1
            for k in range(len(predictors)):
                prob = confusion_matrices[k][j][predictions[k]]
                likelihood_of_label *= prob
            M[i][j] = likelihood_of_label

        # Normalize to 1. (i.e. Convert to probabilities)
        M[i, :] /= M[i, :].sum()

    # M Step, update confusion matrices
    for j in range(len(predictors)):
        for k in range(len(class_labels)):
            for m in range(len(class_labels)):
                numerator = 0
                denominator = 0
                for i in range(len(dataset)):
                    denominator += M[i][k]
                    if predictions_matrix[j][i] != m:
                        continue
                    numerator += M[i][k]
                confusion_matrices[j][k][m] = numerator / denominator

    # Now we'll take the predictions and gather precision/recall/accuracy metrics using ReaL labels as ground truth
    generated_predictions = []
    for row in range(len(M)):
        max_index = 0
        max_value = 0
        for i in range(len(M[row])):
            if M[row][i] > max_value:
                max_index = i
                max_value = M[row][i]
        generated_predictions.append((
            dataset[row][0],
            class_labels[max_index],
            max_value
        ))

    # Accuracy
    total_correct = 0
    for prediction in generated_predictions:
        if real_prediction_dict[prediction[0]] == prediction[1]:
            total_correct += 1
    accuracies.append(total_correct / len(dataset))

    # Precision, recall (averaged over classes)
    class_precisions: list[float] = []
    class_recalls: list[float] = []
    for c in class_labels:
        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0
        for i in range(len(generated_predictions)):
            if dataset[i][1] == c:
                if generated_predictions[i][1] == c:
                    true_positives += 1
                else:
                    false_negatives += 1
            else:
                if generated_predictions[i][1] == c:
                    false_positives += 1
                else:
                    true_negatives += 1

        class_precisions.append(true_positives / (true_positives + false_positives))
        class_recalls.append(true_positives / (true_positives + false_negatives))

    precisions.append(sum(class_precisions) / len(class_precisions))
    recalls.append(sum(class_recalls) / len(class_recalls))

end_time = time.time()

print("Dumping confusion matrices")
for i in range(len(confusion_matrices)):
    np.savetxt(
        "results/confusion_matrices/confusion_matrix_" + str(i),
        confusion_matrices[i],
        delimiter=','
    )

predictor_agreement_heatmap = np.zeros((len(predictors), len(predictors)))

print("Dumping predictor agreement heatmap")
for pi in range(len(predictors)):
    for pj in range(len(predictors)):
        total_agreed = 0
        for i in range(len(dataset)):
            if predictors[pi].predict_image(dataset[i][0]) == predictors[pj].predict_image(dataset[i][0]):
                total_agreed += 1
        predictor_agreement_heatmap[pi][pj] = total_agreed / len(dataset)

np.savetxt(
    "results/predictor_agreement_heatmap",
    predictor_agreement_heatmap,
    delimiter=","
)

print("Dumping predictions with confidence scores")
labeled_data_with_confidences_file = open("results/labeled_data_with_confidences", "w")

for prediction in generated_predictions:
    print(";".join([str(p) for p in prediction]), file=labeled_data_with_confidences_file)
labeled_data_with_confidences_file.close()


plt.figure()
print("Generating accuracy/epoch plot")
plt.plot(list(range(1, len(accuracies) + 1)), accuracies, label="Accuracy")
plt.title("Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.savefig("results/accuracy.png")
plt.close()

plt.figure()
print("Generating precision/epoch plot")
plt.plot(list(range(1, len(precisions) + 1)), precisions, label="Precision")
plt.title("Precision")
plt.xlabel("Epoch")
plt.ylabel("Precision")
plt.savefig("results/precision.png")
plt.close()

plt.figure()
print("Generating recall/epoch plot")
plt.plot(list(range(1, len(recalls) + 1)), recalls, label="Recall")
plt.title("Recall")
plt.xlabel("Epoch")
plt.ylabel("recall")
plt.savefig("results/recall.png")
plt.close()

print("Class label order")
print(";".join(class_labels))
print("Predictor order")
print("gpt4.1 nano,gpt4.1 mini,grok2,gpt4o")

print("Annotator overall expertise")
for confusion_matrix in confusion_matrices:
    average_diag = np.trace(confusion_matrix) / confusion_matrix.shape[0]
    print(average_diag)

print(f"Execution time: {end_time - start_time:.3f} seconds")
