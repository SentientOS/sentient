import tflite_model_maker as mm
from tflite_model_maker.text_classifier import BertClassifierSpec, DataLoader
import tensorflow as tf

# Use the BERT model spec
spec = BertClassifierSpec()

# Load CSV dataset
data = DataLoader.from_csv(
    filename="augmented_log_dataset.csv",
    model_spec=spec,
    text_column="text",
    label_column="label"
)

# Split the dataset
train_data, test_data = data.split(0.8)

# Train the model
model = mm.text_classifier.create(
    train_data=train_data,
    model_spec=spec,
    validation_data=test_data,
    epochs=5,
    batch_size=32
)

# Evaluate the model
loss, acc = model.evaluate(test_data)
print(f"\n✅ Evaluation Accuracy: {acc:.4f}")

# Export the model
model.export(export_dir='model')

