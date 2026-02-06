from flask import Flask, request, jsonify
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

X_latent = []
y_labels = []
classifier = LogisticRegression()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Privacy-Preserving ML Cloud Server",
        "status": "running",
        "endpoints": {
            "upload_latent": "POST /upload_latent",
            "train": "POST /train", 
            "predict": "POST /predict"
        },
        "samples_stored": len(X_latent)
    })

@app.route("/upload_latent", methods=["POST"])
def upload_latent():
    data = request.json
    X_latent.append(data["latent_vector"])
    y_labels.append(data["label"])
    return jsonify({"status": "latent stored"})

@app.route("/train", methods=["POST"])
def train():
    classifier.fit(np.array(X_latent), np.array(y_labels))
    return jsonify({"status": "model trained", "samples": len(X_latent)})

@app.route("/predict", methods=["POST"])
def predict():
    latent = np.array(request.json["latent_vector"]).reshape(1, -1)
    pred = classifier.predict(latent)[0]
    confidence = classifier.predict_proba(latent).max()
    return jsonify({
        "prediction": int(pred),
        "confidence": float(confidence)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)