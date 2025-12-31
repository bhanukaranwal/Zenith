import pandas as pd
import numpy as np
from pathlib import Path

output_dir = Path("data/examples")
output_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

n_samples = 10000
customer_data = pd.DataFrame({
    'customer_id': range(1, n_samples + 1),
    'age': np.random.randint(18, 80, n_samples),
    'income': np.random.randint(20000, 200000, n_samples),
    'credit_score': np.random.randint(300, 850, n_samples),
    'account_balance': np.random.uniform(0, 50000, n_samples),
    'num_transactions': np.random.randint(0, 100, n_samples),
    'tenure_months': np.random.randint(1, 120, n_samples),
    'churn': np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
})

customer_data.to_csv(output_dir / "customer_data.csv", index=False)
print(f"Created customer_data.csv with {n_samples} samples")

n_images = 1000
image_metadata = pd.DataFrame({
    'image_id': range(1, n_images + 1),
    'category': np.random.choice(['cat', 'dog', 'bird', 'fish'], n_images),
    'width': np.random.randint(200, 1024, n_images),
    'height': np.random.randint(200, 1024, n_images),
    'file_size_kb': np.random.randint(50, 5000, n_images)
})

image_metadata.to_csv(output_dir / "image_metadata.csv", index=False)
print(f"Created image_metadata.csv with {n_images} samples")

n_texts = 5000
text_data = pd.DataFrame({
    'text_id': range(1, n_texts + 1),
    'text': [f"Sample text document {i} with some content" for i in range(1, n_texts + 1)],
    'sentiment': np.random.choice(['positive', 'negative', 'neutral'], n_texts),
    'length': np.random.randint(50, 500, n_texts)
})

text_data.to_csv(output_dir / "text_data.csv", index=False)
print(f"Created text_data.csv with {n_texts} samples")

print("\nExample data created successfully!")
print(f"Data saved to: {output_dir.absolute()}")
