import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


def main():
    print("Zenith Tabular ML Example")
    print("=" * 50)
    
    data = pd.read_csv("data/examples/customer_data.csv")
    print(f"Loaded dataset: {data.shape[0]} rows, {data.shape[1]} columns")
    
    X = data.drop(['customer_id', 'churn'], axis=1)
    y = data['churn']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    print("\nFeature Importance:")
    for feature, importance in zip(X.columns, model.feature_importances_):
        print(f"{feature}: {importance:.4f}")


if __name__ == "__main__":
    main()
