import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Two lists one for evidence and the other for labels
    evidence = []
    labels = []

    # Key-value dictionary that will map the month to a number
    month = {"Jan": 0, "Feb": 1, "Mar": 2, "April": 3, "May": 4, "June": 5,
             "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}

    # Reading the csv file
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)

        # Skip the first row of the file
        next(reader)

        # For every row in the file
        for row in reader:

            # Adding every element in the row as discribed above
            evidence.append((
                [int(row[0]), float(row[1]), int(row[2]), float(row[3]), int(row[4]), float(row[5])] +
                [float(e) for e in row[6:9]] + [month[row[10]]] +
                [int(e) for e in row[11:14]] + [0 if row[15] == "New_Visitor" else 1] +
                [1 if row[16] == "TRUE" else 0]
            ))

            # Adding the label (output)
            labels.append(1 if row[17] == "TRUE" else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # This will return a K nearest neighbor classifier model
    model = KNeighborsClassifier(n_neighbors=1)

    # training the model with the training data
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # The count of how many times the prediction matches the label whewn it is TRUE
    correct_positive_match = len([
        prediction for (label, prediction) in zip(labels, predictions) if label == 1 and label == prediction
    ])

    # Count of how many labels are TRUE
    num_positive_labels = len([label for label in labels if label == 1])

    # The count of how many times the prediction matches the label whewn it is FALSE
    correct_negative_match = len([
        prediction for (label, prediction) in zip(labels, predictions) if label == 0 and label == prediction
    ])

    # Count of how many labels are FALSE
    num_negative_labels = len([label for label in labels if label == 0])

    # True positive rate
    sensitivity = correct_positive_match / num_positive_labels

    # True Negative rate
    specificity = correct_negative_match / num_negative_labels

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
