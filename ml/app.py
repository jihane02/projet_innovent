from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

app = Flask(__name__)

@app.route("/train", methods=["POST"])
def train_model():

    print (1)
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the file into a pandas DataFrame
        print (2)
        df = pd.read_csv(file)
        # Assuming the last column is the target variable
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values

        # Splitting the dataset into the Training set and Test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Fitting Decision Tree to the Training set
        classifier = DecisionTreeClassifier(random_state=0)
        classifier.fit(X_train, y_train)

        # Saving the model
        joblib.dump(classifier, "decision_tree_model.pkl")

        return jsonify({"message": "Model trained successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    sepal_length = data.get("sepal_length", 0)
    sepal_width = data.get("sepal_width", 0)
    petal_length = data.get("petal_length", 0)
    petal_width = data.get("petal_width", 0)

    pred_args = [sepal_length, sepal_width, petal_length, petal_width]
    pred_args_arr = np.array(pred_args).reshape(1, -1)

    ml_model = joblib.load("decision_tree_model.pkl")
    model_prediction = ml_model.predict(pred_args_arr)

    return jsonify({"prediction": model_prediction[0]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
