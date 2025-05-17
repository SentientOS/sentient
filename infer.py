import time
import numpy as np
import tensorflow_hub as hub
import tensorflow_text as text
from tensorflow.lite.python.interpreter import Interpreter

# Use the same preprocessing model used during training
PREPROCESS_MODEL = "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
preprocessor = hub.load(PREPROCESS_MODEL)

# Load TFLite model
MODEL_PATH = "model/model.tflite"
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess(log_line):
    # Tokenize using the BERT preprocessor
    encoding = preprocessor([log_line])
    return (
        np.array(encoding["input_word_ids"], dtype=np.int32),
        np.array(encoding["input_mask"], dtype=np.int32),
        np.array(encoding["input_type_ids"], dtype=np.int32),
    )

def classify_log(log_line: str) -> str:
    input_ids, input_mask, segment_ids = preprocess(log_line)

    interpreter.set_tensor(input_details[0]['index'], input_ids)
    interpreter.set_tensor(input_details[1]['index'], input_mask)
    interpreter.set_tensor(input_details[2]['index'], segment_ids)

    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    prediction = np.argmax(output_data[0])
    return ["SAFE", "WARNING", "THREAT"][prediction]

def monitor_logs():
    print("[Sentient] Monitoring logs for AI-based threat detection...")
    LOG_FILE = "test.log"

    try:
        with open(LOG_FILE, "r") as log_file:
            while True:
                line = log_file.readline()
                if not line:
                    time.sleep(0.5)
                    continue

                result = classify_log(line)
                if result != "SAFE":
                    print(f"[Sentient {result}] {line.strip()}")
    except FileNotFoundError:
        print(f"[Sentient] Error: Log file '{LOG_FILE}' not found.")
    except KeyboardInterrupt:
        print("[Sentient] Exiting log monitor.")

if __name__ == "__main__":
    monitor_logs()

