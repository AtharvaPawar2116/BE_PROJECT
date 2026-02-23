from pathlib import Path
import json


def main():
    """Train CNN model for multiple soil types (+ optional non_soil_human class)."""

    import numpy as np
    import matplotlib.pyplot as plt
    from tensorflow.keras import layers, models
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    basepath = Path("dataset")
    train_dir = basepath / "train"
    test_dir = basepath / "test"

    if not train_dir.exists() or not test_dir.exists():
        raise FileNotFoundError(
            "Dataset folders not found. Expected structure: dataset/train/<class> and dataset/test/<class>."
        )

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        rotation_range=15,
    )
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)

    training_set = train_datagen.flow_from_directory(
        str(train_dir), target_size=(100, 100), batch_size=32, class_mode="categorical"
    )
    test_set = test_datagen.flow_from_directory(
        str(test_dir), target_size=(100, 100), batch_size=32, class_mode="categorical"
    )

    class_count = training_set.num_classes
    model = models.Sequential(
        [
            layers.Conv2D(32, (3, 3), activation="relu", input_shape=(100, 100, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.4),
            layers.Dense(class_count, activation="softmax"),
        ]
    )

    model.compile(optimizer=Adam(learning_rate=0.001), loss="categorical_crossentropy", metrics=["accuracy"])

    steps_per_epoch = int(np.ceil(training_set.samples / 32))
    val_steps = int(np.ceil(test_set.samples / 32))

    history = model.fit(
        training_set,
        steps_per_epoch=steps_per_epoch,
        epochs=25,
        validation_data=test_set,
        validation_steps=val_steps,
    )

    basepath.mkdir(parents=True, exist_ok=True)
    model_path = basepath / "soil_model_cnn.h5"
    model.save(str(model_path))

    test_score = model.evaluate(test_set, verbose=1)
    train_score = model.evaluate(training_set, verbose=1)

    plt.figure()
    plt.plot(history.history["accuracy"])
    plt.plot(history.history["val_accuracy"])
    plt.title("Model Accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("Epoch")
    plt.legend(["Train", "Validation"], loc="upper left")
    plt.savefig(basepath / "accuracy.png", bbox_inches="tight")

    plt.figure()
    plt.plot(history.history["loss"])
    plt.plot(history.history["val_loss"])
    plt.title("Model Loss")
    plt.ylabel("Loss")
    plt.xlabel("Epoch")
    plt.legend(["Train", "Validation"], loc="upper left")
    plt.savefig(basepath / "loss.png", bbox_inches="tight")

    class_map = {v: k for k, v in training_set.class_indices.items()}
    class_index_path = basepath / "class_indices.json"
    with open(class_index_path, "w", encoding="utf-8") as fp:
        json.dump(training_set.class_indices, fp, indent=2)

    has_non_soil = any("non_soil" in name.lower() or "human" in name.lower() for name in class_map.values())

    msg = (
        f"Training Accuracy: {train_score[1] * 100:.2f}%\n"
        f"Testing Accuracy: {test_score[1] * 100:.2f}%\n"
        f"Classes Learned ({class_count}): {', '.join(class_map.values())}\n"
        f"Model Saved: {model_path}\n"
        f"Class Index Saved: {class_index_path}\n"
    )

    if not has_non_soil:
        msg += (
            "Warning: Add a non_soil_human class in dataset to improve rejection of human/non-soil images."
        )

    return msg


if __name__ == "__main__":
    print(main())
