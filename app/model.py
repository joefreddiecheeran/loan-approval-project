import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Define file paths
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'loan_data.csv')
MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'model_pipeline.pkl')

def train_model():
    """
    Trains the loan approval prediction model and saves it.
    """
    print("--- Starting Model Training ---")

    # 1. Load Data
    try:
        df = pd.read_csv(DATA_FILE_PATH)
        print("Dataset loaded successfully.")
    except FileNotFoundError:
        print(f"Error: Dataset not found at {DATA_FILE_PATH}. Please ensure the data is in the correct directory.")
        return

    # Drop Loan_ID as it's not a feature
    df = df.drop('Loan_ID', axis=1)

    # 2. Preprocessing
    # Separate target variable
    X = df.drop('Loan_Status', axis=1)
    y = df['Loan_Status']

    # Encode the target variable
    le = LabelEncoder()
    y = le.fit_transform(y)

    # Identify categorical and numerical features
    categorical_features = X.select_dtypes(include=['object']).columns
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
    
    print(f"Categorical features: {list(categorical_features)}")
    print(f"Numerical features: {list(numerical_features)}")

    # Create preprocessing pipelines for numerical and categorical data
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')), # Use median for robustness to outliers
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')) # Ignore unknown categories during prediction
    ])

    # Create a preprocessor object using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough' # Keep other columns (if any)
    )

    # 3. Define the Model
    # Using RandomForest for good performance out-of-the-box
    model = RandomForestClassifier(n_estimators=100, random_state=42, oob_score=True)

    # 4. Create the Full Pipeline
    # This pipeline encapsulates preprocessing and modeling
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    # 5. Split Data and Train the Model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training the model pipeline...")
    model_pipeline.fit(X_train, y_train)
    print("Model training complete.")

    # 6. Evaluate the Model
    y_pred = model_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set: {accuracy:.4f}")
    if hasattr(model, 'oob_score_'):
        print(f"Model OOB Score: {model_pipeline.named_steps['classifier'].oob_score_:.4f}")


    # 7. Save the Model Pipeline
    joblib.dump(model_pipeline, MODEL_FILE_PATH)
    print(f"Model pipeline saved to {MODEL_FILE_PATH}")
    print("--- Model Training Finished ---")

if __name__ == '__main__':
    # This allows the script to be run directly to train the model
    train_model()