from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

try:
    with open("model.pkl", "rb") as f:
        model = joblib.load(f)
except Exception as e:
    model = None
    load_error = str(e)

app = FastAPI()

class WineInput(BaseModel):
    features: list[float]

@app.post("/predict")
def predict_quality(data: WineInput):
    if model is None:
        return {"error": f"Model failed to load: {load_error}"}

    all_columns = [
        "fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides",
        "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol"
    ]
    
    df_input = pd.DataFrame([data.features], columns=all_columns)

    
    sorted_features_by_importance = [
        "alcohol", "volatile acidity", "sulphates", "citric acid", 
        "total sulfur dioxide", "density", "chlorides", "fixed acidity", 
        "pH", "free sulfur dioxide", "residual sugar"
    ]
    
    try:
        n_features = model.n_features_in_
        
        final_features = sorted_features_by_importance[:n_features]
        
        input_data = df_input[final_features]
        
        # Predict
        prediction = model.predict(input_data)
        
        return {
            "name": "Vamsi Krishna",       
            "roll_no": "2022BCD0022",      
            "wine_quality": int(prediction[0])
        }

    except Exception as e:
        return {
            "error": "Prediction Failed",
            "details": str(e),
            "model_expects": getattr(model, "n_features_in_", "Unknown")
        }
    
#comment