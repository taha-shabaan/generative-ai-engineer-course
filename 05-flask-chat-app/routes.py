import logging
from flask import Blueprint, request, render_template, session, url_for, redirect
from flask.json import jsonify
import agent
import uuid
api_bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)



def parse_location(raw_location):
    """Validate optional GPS coordinates from the client."""
    if not isinstance(raw_location, dict): # isinstance
        return None
    try:
        lat = float(raw_location["lat"])
        lon = float(raw_location["lon"])
    except (KeyError, TypeError, ValueError):
        return None

    if -90 <= lat <= 90 and -180 <= lon <= 180:
        return {"lat": lat, "lon": lon}
    return None

@api_bp.route("/", methods=["GET"])
def get_home():
    if  "messages" not in session:
        session["messages"] = []
    return render_template('chat.html', messages=session["messages"])

# health route
@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"}), 200


@api_bp.route("/api/chat", methods=["POST"])
def chat():
    # Accept both JSON (fetch/curl) and HTML form submissions
    data = request.get_json(silent=True) or request.form
    message = data.get("message", "")
    location = parse_location(data.get("location"))

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Provide a non-empty 'message' string."}), 400

    try:
        user_message = message.strip()
        print("agent running wait......")
        print("user_message:", user_message)
        print(session['messages'])

        session.setdefault("messages", [])
        session["messages"].append({"type": "user", "message": user_message})
        session['user_location'] = location
        session.modified = True

        reply = agent.run_agent(user_message, str(uuid.uuid4()))

        session["messages"].append({"type": "ai", "message": reply})
        session.modified = True

        if request.is_json:
            return jsonify({"response": reply})
        return redirect('/')

    except Exception:
        logger.exception("LangChain agent failed during /api/chat")
        return jsonify({"error": "The AI agent encountered an error. Please try again."}), 500
