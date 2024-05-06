import gzip
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

def preprocess_data(data):
    print(data.isnull().sum())

    features = data.drop(columns=['Dropout'])
    target = data['Dropout']

    numeric_features = features.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = features.select_dtypes(include=['object']).columns
    categorical_features = [col for col in categorical_features if col != 'Dropout']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    X_train = preprocessor.fit_transform(features)
    y_train = target

    with gzip.open('../../models/scaler.gz', 'wb') as f:
        joblib.dump(preprocessor.named_transformers_['num'].named_steps['scaler'], f)

    return X_train, y_train, preprocessor

def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def save_model(model, filepath):
    joblib.dump(model, filepath)
    print("Model je bil uspešno shranjen.")

def main():
    data = pd.read_csv("../../data/processed/current_data.csv")
    X_train, y_train, preprocessor = preprocess_data(data)
    model = train_model(X_train, y_train)

    save_model(model, "../../models/random_forest_model.keras")

if __name__ == "__main__":
    main()
