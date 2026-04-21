
from flask import Flask, render_template, request
import os
import joblib
import pandas as pd

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

crop_model_path = os.path.join(MODEL_DIR, "xgboost_crop_model.pkl")
feature_columns_path = os.path.join(MODEL_DIR, "features_column.pkl")

crop_model = joblib.load(crop_model_path)
feature_columns = joblib.load(feature_columns_path)


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


@app.route("/predict-crop", methods=["POST"])
def predict_crop():
    try:
        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])

        input_data = {
            "N": N,
            "P": P,
            "K": K,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }

        input_df = pd.DataFrame([input_data])

        # Ensure same column order as training
        input_df = input_df[feature_columns]

        prediction = crop_model.predict(input_df)
        predicted_crop = prediction[0]

        return render_template(
            "result.html",
            module_name="Crop Recommendation",
            prediction_text=f"Recommended Crop: {predicted_crop}",
            N=N,
            P=P,
            K=K,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall
        )

    except Exception as e:
        return render_template(
            "result.html",
            module_name="Crop Recommendation",
            prediction_text=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    app.run(debug=True)