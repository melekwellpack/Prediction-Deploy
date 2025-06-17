# main.py
from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import joblib
from huggingface_hub import hf_hub_download

# Import your three Blueprints
from generate_sms_api           import generate_sms_api   # your SMS‐generation blueprint
from flask_app     import predict_bp         # your prediction blueprint
from schedule_app   import schedule_bp

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ——————————————————————————————————————
# App configuration
# ——————————————————————————————————————
app.secret_key = "sms_success_prediction_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"

# ——————————————————————————————————————
# Load model from Hugging Face Hub
# ——————————————————————————————————————
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

REPO_ID = "Wellpack/Stage_1_Project"
FILENAME = "sms_models.pkl"
print("Downloading model from Hugging Face...")
# Download from Hugging Face
model_path = hf_hub_download(repo_id=REPO_ID, 
                             filename=FILENAME,
                             token=HUGGINGFACE_TOKEN)

print(f"Model downloaded to: {model_path}")

# Load the model
with open(model_path, "rb") as f:
    models = joblib.load(f)

print("Model loaded successfully!")

# Store model in Flask config for access in Blueprints
app.config['MODEL_PATH'] = model_path
app.config['MODELS'] = models 

# Optional: tighten CORS if you’re hosting front‐end separately
CORS(app)

# ——————————————————————————————————————
# Routes
# ——————————————————————————————————————
@app.route("/")
def index():
    # your landing page (webPage_simple.html) lives in templates/
    return render_template("webPage_simple.html")

# ——————————————————————————————————————
# Blueprint registration
# ——————————————————————————————————————
# Mount your SMS‐generation endpoints
app.register_blueprint(generate_sms_api)
# Mount your prediction/upload endpoints
app.register_blueprint(predict_bp)
# register new scheduling blueprint
app.register_blueprint(schedule_bp)

# ——————————————————————————————————————
# Entry point
# ——————————————————————————————————————
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
