from flask import Flask, render_template, request, jsonify
import os
import joblib
import pandas as pd
from catboost import CatBoostClassifier, Pool

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# =========================
# Load Crop Model
# =========================
crop_model = joblib.load(os.path.join(MODEL_DIR, "xgboost_crop_model.pkl"))
feature_columns = joblib.load(os.path.join(MODEL_DIR, "features_column.pkl"))

# =========================
# Load Fertilizer Model
# =========================
fertilizer_model = joblib.load(os.path.join(MODEL_DIR, "fertilizer_model.pkl"))
fertilizer_label_encoder = joblib.load(os.path.join(MODEL_DIR, "fertilizer_label_encoder.pkl"))

# =========================
# Load Yield Model
# =========================
yield_model = joblib.load(os.path.join(MODEL_DIR, "yield_model.pkl"))

# =========================
# Load Irrigation Model
# =========================
irrigation_model = CatBoostClassifier()
irrigation_model.load_model(os.path.join(MODEL_DIR, "irrigation_model.cbm"))

irrigation_cat_cols = [
    "Soil_Type",
    "Crop_Type",
    "Crop_Growth_Stage",
    "Season",
    "Irrigation_Type",
    "Water_Source",
    "Mulching_Used",
    "Region"
]


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/crop")
def crop_page():
    return render_template("crop.html")


@app.route("/fertilizer")
def fertilizer_page():
    return render_template("fertilizer.html")


@app.route("/yield")
def yield_page():
    return render_template("yield.html")


@app.route("/irrigation")
def irrigation_page():
    return render_template("irrigation.html")


@app.route("/predict-crop", methods=["POST"])
def predict_crop():
    try:
        input_df = pd.DataFrame([{
            "N": float(request.form["N"]),
            "P": float(request.form["P"]),
            "K": float(request.form["K"]),
            "temperature": float(request.form["temperature"]),
            "humidity": float(request.form["humidity"]),
            "ph": float(request.form["ph"]),
            "rainfall": float(request.form["rainfall"])
        }])

        input_df = input_df[feature_columns]
        prediction = crop_model.predict(input_df)[0]

        return render_template(
            "result.html",
            module_name="Crop Recommendation",
            prediction_text=f"Recommended Crop: {prediction}"
        )

    except Exception as e:
        return render_template(
            "result.html",
            module_name="Crop Recommendation",
            prediction_text=f"Error: {str(e)}"
        )


@app.route("/predict-fertilizer", methods=["POST"])
def predict_fertilizer():
    try:
        data = request.get_json()

        input_df = pd.DataFrame([{
            "Soil_Type": data["Soil_Type"],
            "Soil_pH": float(data["Soil_pH"]),
            "Soil_Moisture": float(data["Soil_Moisture"]),
            "Organic_Carbon": float(data["Organic_Carbon"]),
            "Electrical_Conductivity": float(data["Electrical_Conductivity"]),
            "Nitrogen_Level": int(data["Nitrogen_Level"]),
            "Phosphorus_Level": int(data["Phosphorus_Level"]),
            "Potassium_Level": int(data["Potassium_Level"]),
            "Temperature": float(data["Temperature"]),
            "Humidity": float(data["Humidity"]),
            "Rainfall": float(data["Rainfall"]),
            "Crop_Type": data["Crop_Type"],
            "Crop_Growth_Stage": data["Crop_Growth_Stage"],
            "Season": data["Season"],
            "Irrigation_Type": data["Irrigation_Type"],
            "Previous_Crop": data["Previous_Crop"],
            "Region": data["Region"],
            "Fertilizer_Used_Last_Season": float(data["Fertilizer_Used_Last_Season"]),
            "Yield_Last_Season": float(data["Yield_Last_Season"])
        }])

        prediction = fertilizer_model.predict(input_df)
        fertilizer_name = fertilizer_label_encoder.inverse_transform(prediction)[0]

        return jsonify({
            "success": True,
            "recommended_fertilizer": fertilizer_name
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


@app.route("/predict-yield", methods=["POST"])
def predict_yield():
    try:
        data = request.get_json()

        input_df = pd.DataFrame([{
            "Crop": data["Crop"],
            "Region": data["Region"],
            "Soil_Type": data["Soil_Type"],
            "Soil_pH": float(data["Soil_pH"]),
            "Rainfall_mm": float(data["Rainfall_mm"]),
            "Temperature_C": float(data["Temperature_C"]),
            "Humidity_pct": float(data["Humidity_pct"]),
            "Fertilizer_Used_kg": float(data["Fertilizer_Used_kg"]),
            "Irrigation": data["Irrigation"],
            "Pesticides_Used_kg": float(data["Pesticides_Used_kg"]),
            "Planting_Density": float(data["Planting_Density"]),
            "Previous_Crop": data["Previous_Crop"]
        }])

        prediction = yield_model.predict(input_df)[0]

        return jsonify({
            "success": True,
            "predicted_yield": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


@app.route("/predict-irrigation", methods=["POST"])
def predict_irrigation():
    try:
        data = request.get_json()

        input_df = pd.DataFrame([{
            "Soil_Type": data["Soil_Type"],
            "Soil_pH": float(data["Soil_pH"]),
            "Soil_Moisture": float(data["Soil_Moisture"]),
            "Organic_Carbon": float(data["Organic_Carbon"]),
            "Electrical_Conductivity": float(data["Electrical_Conductivity"]),
            "Temperature_C": float(data["Temperature_C"]),
            "Humidity": float(data["Humidity"]),
            "Rainfall_mm": float(data["Rainfall_mm"]),
            "Crop_Type": data["Crop_Type"],
            "Crop_Growth_Stage": data["Crop_Growth_Stage"],
            "Season": data["Season"],
            "Sunlight_Hours": float(data["Sunlight_Hours"]),
            "Wind_Speed_kmh": float(data["Wind_Speed_kmh"]),
            "Irrigation_Type": data["Irrigation_Type"],
            "Water_Source": data["Water_Source"],
            "Previous_Irrigation_mm": float(data["Previous_Irrigation_mm"]),
            "Field_Area_hectare": float(data["Field_Area_hectare"]),
            "Mulching_Used": data["Mulching_Used"],
            "Region": data["Region"]
        }])

        input_pool = Pool(input_df, cat_features=irrigation_cat_cols)
        prediction = irrigation_model.predict(input_pool)[0]

        return jsonify({
            "success": True,
            "irrigation_need": str(prediction)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)