import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# =========================
# 1. Create Output Folder
# =========================
os.makedirs("model_outputs", exist_ok=True)

# =========================
# 2. Load Dataset
# =========================
df = pd.read_csv("crop_data.csv")

# =========================
# 3. Data Cleaning
# =========================
df = df.dropna()

#  REMOVE RARE CROPS
crop_counts = df["CROP"].value_counts()
valid_crops = crop_counts[crop_counts >= 2].index
df = df[df["CROP"].isin(valid_crops)]

print("Total crop classes after cleaning:", df["CROP"].nunique())

# Save cleaned dataset
df.to_csv("model_outputs/cleaned_crop_data.csv", index=False)

# =========================
# 4. Features & Target
# =========================
X = df.drop(["CROP"], axis=1)
y = df["CROP"]

# =========================
# 5. Column Types
# =========================
categorical_features = ["STATE", "SOIL_TYPE"]
numerical_features = [
    "N_SOIL", "P_SOIL", "K_SOIL",
    "TEMPERATURE", "HUMIDITY", "ph", "RAINFALL"
]

# =========================
# 6. Preprocessing
# =========================
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ("num", "passthrough", numerical_features)
])

# =========================
# 7. Model
# =========================
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ))
])

# =========================
# 8. Train-Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# 9. Train Model
# =========================
print("Training Crop Recommendation Model...")
model.fit(X_train, y_train)

# =========================
# 10. Evaluation
# =========================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred) 

print("\nAccuracy:", accuracy)
print("\nClassification Report:\n", report)

a = report + f"Model Accuracy: {accuracy:.4f}"
# 🔹 Save Accuracy to file
# with open("model_outputs/accuracy.txt", "w") as f:
#     f.write(f"Model Accuracy: {accuracy:.4f}")

# 🔹 Save Classification Report to file
with open("model_outputs/classification_report.txt", "w") as f:
    f.write(a)

# =========================
# 11. Confusion Matrix
# =========================
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, cmap="Blues")
plt.title("Confusion Matrix – Crop Recommendation")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("model_outputs/confusion_matrix.png")
plt.show()

# =========================
# 12. Accuracy Graph
# =========================
plt.figure(figsize=(4, 4))
plt.bar(["Random Forest"], [accuracy])
plt.ylim(0, 1)
plt.ylabel("Accuracy")
plt.title("Model Accuracy")
plt.savefig("model_outputs/accuracy.png")
plt.show()

# =========================
# 13. Save Model
# =========================
joblib.dump(model, "model_outputs/crop_recommendation_model.pkl")

print("\nTraining completed successfully.")
