import os
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from typing import Tuple

DURATION_TO_MINUTES = {
    "Curto (até 90min)": (0, 90),
    "Médio (90-120min)": (90, 120),
    "Longo (120min+)": (120, 9999)
}

DECADE_TO_YEARS = {
    "Qualquer época": None,
    "Clássico (antes de 2000)": (0, 1999),
    "Anos 2000": (2000, 2009),
    "Recente (após 2010)": (2010, 9999)
}

class MapTheSoulTrainer:
    """
    A pipeline to train a Decision Tree model to predict movie recommendations
    based on the IMDB Top 1000 dataset.
    """
    def __init__(self, features: list['str'], target: str, data_path: str = "data/imdb_top_1000.csv", output_dir: str = "data"):
        self._data_path = data_path
        self._output_dir = output_dir
        self._model = None
        self._label_encoder = LabelEncoder()
        self._features = features
        self._target = target

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def run_pipeline(self):
        """Executes the full workflow from loading to saving."""
        df = self._load_and_prepare()
        x_test, y_test = self.train(df)
        self.evaluate(x_test, y_test)
        self.save_artifacts()
        self.save_model()

    def _load_and_prepare(self) -> pd.DataFrame:
        if not os.path.exists(self._data_path):
            raise FileNotFoundError(f"Dataset not found at {self._data_path}")

        df_raw = pd.read_csv(self._data_path)

        # Select required columns and drop nulls immediately
        columns = ["Genre", "IMDB_Rating", "Runtime", "Meta_score", "No_of_Votes", "Released_Year"]
        df = df_raw[columns].dropna().copy()

        # Data Cleaning: Handle Runtime and Year strings
        df["Runtime"] = df["Runtime"].str.extract('(\d+)').astype(int)
        df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
        df = df.dropna()

        # Explode Genres: One row per genre for better granularity
        df["Genre"] = df["Genre"].str.split(", ")
        df = df.explode("Genre").reset_index(drop=True)

        # Target variable: Recommended if rating >= 8.0
        df[self._target] = (df["IMDB_Rating"] >= 8.0).astype(int)
        df["Genre_encoded"] = self._label_encoder.fit_transform(df["Genre"])

        return df

    def train(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Trains the Decision Tree model and returns the test set for evaluation."""
        x = df[self._features]
        y = df[self._target]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42, stratify=y
        )

        # Using max_depth to prevent overfitting
        self._model = DecisionTreeClassifier(max_depth=5, criterion="gini", random_state=42)
        self._model.fit(x_train, y_train)

        return x_test, y_test

    def evaluate(self, x_test: pd.DataFrame, y_test: pd.Series) -> None:
        """Evaluates the model and generates metrics and visualizations."""
        if self._model is None:
            raise ValueError("Model has not been trained yet.")

        y_pred = self._model.predict(x_test)

        print("\n" + "="*40)
        print("METRICS REPORT")
        print("="*40)
        print(classification_report(y_test, y_pred))

        self._plot_confusion_matrix(y_test, y_pred)
        self._plot_feature_importance()

    def _plot_confusion_matrix(self, y_test, y_pred):
        """Plots and saves the confusion matrix."""
        plt.figure(figsize=(6, 5))
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='RdPu')
        plt.title("Confusion Matrix")
        plt.savefig(os.path.join(self._output_dir, "confusion_matrix.png"))
        plt.close()

    def _plot_feature_importance(self):
        """Plots and saves the feature importance."""
        importances = self._model.feature_importances_
        plt.figure(figsize=(8, 4))
        plt.barh(self._features, importances, color='teal')
        plt.title("Feature Importance for Recommendations")
        plt.tight_layout()
        plt.savefig(os.path.join(self._output_dir, "feature_importance.png"))
        plt.close()

    def save_artifacts(self) -> None:
        """Saves the label encoder and metadata maps for use in the application."""
        with open(os.path.join(self._output_dir, "label_encoder.pkl"), "wb") as f:
            pickle.dump(self._label_encoder, f)

        # Metadata for the application
        maps = {
            "generos": list(self._label_encoder.classes_),
            "duracao": DURATION_TO_MINUTES,
            "decada": DECADE_TO_YEARS,
        }
        with open(os.path.join(self._output_dir, "maps.pkl"), "wb") as f:
            pickle.dump(maps, f)

    def save_model(self) -> None:
        """Saves the trained model to disk."""
        with open(os.path.join(self._output_dir, "model.pkl"), "wb") as f:
            pickle.dump(self._model, f)
        print(f"\n✅ Pipeline finished. Artifacts saved in: {self._output_dir}")