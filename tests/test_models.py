import joblib

model = joblib.load("models/yield_prediction/yield_prediction_xgb.pkl")

print(type(model))

if hasattr(model, "feature_names_in_"):
    print(model.feature_names_in_)