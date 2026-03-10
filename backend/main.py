from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("models/crop_model.pkl")

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/crop")
def crop_page():
    return render_template("crop.html")

@app.route("/fertilizer")
def fertilizer_page():
    return render_template("fertilizer.html")

@app.route("/irrigation")
def irrigation_page():
    return render_template("irrigation.html")

@app.route("/yield")
def yield_page():
    return render_template("yield.html")

@app.route("/predict", methods=["POST"])
def predict():
    N = float(request.form["N"])
    P = float(request.form["P"])
    K = float(request.form["K"])
    temperature = float(request.form["temperature"])
    humidity = float(request.form["humidity"])
    ph = float(request.form["ph"])
    rainfall = float(request.form["rainfall"])

    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    prediction = model.predict(features)

    return render_template("result.html", crop=prediction[0])

if __name__ == "__main__":
    app.run(debug=True)