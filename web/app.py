from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

ALGO_CONTAINER_URL = "http://algo_container:8080"

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/train", methods=['POST'])
def train_model():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Prepare the file for sending in a POST request
    files = {'file': (file.filename, file.read(), file.content_type)}

    try:
        response = requests.post("http://algo_container:8080/train", files=files)
        response.raise_for_status()  # Raise an error if the request was not successful
        result= response.json()

        # Assuming the prediction is directly the name of the Iris species
        return render_template('result.html',prediction=result)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Adjusted to accept Iris dataset features
        sepal_length = float(request.form.get('sepal_length', 0))
        sepal_width = float(request.form.get('sepal_width', 0))
        petal_length = float(request.form.get('petal_length', 0))
        petal_width = float(request.form.get('petal_width', 0))

        data = {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        }

        response = requests.post("http://algo_container:8080/predict", json=data)
        response.raise_for_status()  # Raise an error if the request was not successful
        prediction = response.json()["prediction"]

        # Assuming the prediction is directly the name of the Iris species
        return render_template('predict.html', prediction=prediction)
    except (requests.RequestException, ValueError) as e:
        return jsonify({"error": str(e)}), 400  # Return an error message and status code 400 for bad request

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
