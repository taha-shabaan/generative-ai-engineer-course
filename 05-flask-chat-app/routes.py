import logging
from flask import Blueprint, request, render_template
from flask.json import jsonify

api_bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

# home
@api_bp.route("/", methods=["GET"])
def get_home():
    return render_template('chat.html')

# health route
@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"}), 200

@api_bp.route("/api/chat", methods=["POST"])
def chat():
    data =request.get_json(silent=True) # {message:""}
    if not data or not isinstance(data.get("message"), str) or not data["message"].strip():
        return jsonify({"error": "Provide a non-empty 'message' string."})
    try:
        api = "run the agent"
        # run agent here
        print(api)
        return jsonify({"chat":"message"})
    except Exception:
        logger.exception("LangChain agent failed during /api/chat")
        return jsonify({"error": "The AI agent encountered an error. Please try again."}), 500
