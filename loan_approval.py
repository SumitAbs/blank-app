import pickle 

import pandas as pd

class LoanApprovalPrediction:
    def __init__(self, model_filename='loan_approval_model.pkl'):
        # Load the model, label encoders, and scaler from the saved file
        with open(model_filename, "rb") as file:
            model_data = pickle.load(file)
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        # Load feature columns from training data (saved during training)
        self.feature_columns = model_data['feature_columns']

    def predict_user_input(self, user_data):
        # Encode categorical fields
        user_data["education"] = self.label_encoders["education"].transform([user_data["education"]])[0]
        user_data["self_employed"] = self.label_encoders["self_employed"].transform([user_data["self_employed"]])[0]

        # Convert to DataFrame
        user_df = pd.DataFrame([user_data])

        # Ensure the column order matches the trained model
        missing_cols = set(self.feature_columns) - set(user_df.columns)
        for col in missing_cols:
            user_df[col] = 0  # Fill missing features with 0

        user_df = user_df[self.feature_columns]  # Reorder columns to match training data
        user_df_scaled = self.scaler.transform(user_df)

        # Get prediction probabilities
        approval_chance = self.model.predict_proba(user_df_scaled)[:, 0][0] * 100
        return approval_chance

# Example usage:
loan_prediction = LoanApprovalPrediction("loan_approval_model.pkl")

# Sample input data
user_data = {
    "cibil_score": 850,
    "income_annum": 500000, #5,00,000
    "loan_amount":  300000, #3,00,000
    "loan_term": 12,
    "luxury_assets_value": 100000, #1,00,000
    "education": "Graduate", 
    "self_employed": "No"
}

approval_chance = loan_prediction.predict_user_input(user_data)
print(f"Chances of Loan Approval: {approval_chance:.2f}%")
