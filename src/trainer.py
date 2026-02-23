from src.domain.model_trainer import MapTheSoulTrainer


def run_training_process():
    """Runs the entire training process for the Map The Soul movie recommendation model."""
    FEATURES = ["Genre_encoded", "Runtime", "Meta_score", "No_of_Votes"]
    TARGET = "Recomendado"

    trainer = MapTheSoulTrainer(
        features=FEATURES,
        target=TARGET,
        data_path="data/raw/raw.csv",
        output_dir="models"
    )

    print("Starting the training process...")
    trainer.run_pipeline()
    print("Training process completed successfully!")

if __name__ == "__main__":
    run_training_process()