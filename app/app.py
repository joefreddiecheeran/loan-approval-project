from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load the trained model pipeline
MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'model_pipeline.pkl')

try:
    model = joblib.load(MODEL_FILE_PATH)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_FILE_PATH}. Please train the model first by running model.py.")
    model = None

# Define the expected feature order/columns from the training
# This is crucial for creating the prediction DataFrame correctly
EXPECTED_COLUMNS = [
    'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
    'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
    'Credit_History', 'Property_Area'
]

@app.route('/')
def home():
    """Renders the home page with the input form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Receives form data, makes a prediction, and returns the result."""
    if model is None:
        return jsonify({'error': 'Model not loaded. Please check server logs.'}), 500

    try:
        # Get data from the form
        form_data = request.form.to_dict()
        
        # Convert data types for numerical features
        form_data['ApplicantIncome'] = int(form_data['ApplicantIncome'])
        form_data['CoapplicantIncome'] = float(form_data['CoapplicantIncome'])
        form_data['LoanAmount'] = float(form_data['LoanAmount'])
        form_data['Loan_Amount_Term'] = float(form_data['Loan_Amount_Term'])
        form_data['Credit_History'] = float(form_data['Credit_History'])
        
        # Create a DataFrame from the form data
        # Ensure the columns are in the same order as during training
        input_df = pd.DataFrame([form_data], columns=EXPECTED_COLUMNS)
        
        print("Input DataFrame for prediction:\n", input_df)

        # Make prediction
        prediction_code = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]

        # Interpret the prediction
        result_text = "Approved" if prediction_code == 1 else "Rejected"
        confidence = prediction_proba[prediction_code]

        # Prepare response
        response = {
            'prediction': result_text,
            'confidence': f"{confidence:.2f}"
        }
        
        return jsonify(response)

    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # For local development testing
    app.run(debug=True)