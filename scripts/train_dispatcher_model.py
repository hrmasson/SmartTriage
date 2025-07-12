import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os


from config.api_config import settings

def read_dataset() -> pd.DataFrame:
    file_path = settings.DISPATCHER_PROBLEM_DATASET_PATH
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    return pd.read_json(file_path)

def train_model() -> None:
    df = read_dataset()

    # Features/ Target
    df['full_text'] = df['problem'] + ' ' + df['category']
    X = df['full_text']
    y = df['department']

    # Encoding department labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', DecisionTreeClassifier(random_state=42))
    ])

    # Train the model
    pipeline.fit(X_train, y_train)

    # Predict on the test
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.3f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    # Save the model
    joblib.dump(pipeline, settings.DISPATCHER_MODEL_PATH)
    joblib.dump(label_encoder, settings.DISPATCHER_LABELS_PATH)
    print(f"Model and labels have been saved")


if __name__ == "__main__":
    train_model()