from decimal import SPEC_VERSION
import logging
from flask import Blueprint, request, render_template, session, url_for, redirect
from flask.json import jsonify
import agent
api_bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)



# def run_agent(message):
#     # 1. Build the exact path to main-postgres.py in the sibling folder
#     agent_file = Path(__file__).resolve().parent.parent / "04-agent-memory-sqlite-postgres" / "main-postgres.py"
#
#     # 2. Load the file dynamically as a module
#     spec = importlib.util.spec_from_file_location("main_postgres", agent_file)
#     if spec is None or spec.loader is None:
#         raise ImportError(f"Could not load module from {agent_file}")
#
#     main_postgres = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(main_postgres)
#
#     # 3. Access your function!
#     run_agent = main_postgres.run_agent(message)
#     print("agent output::\n", run_agent)


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
    message = data.get("message")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Provide a non-empty 'message' string."}), 400

    try:
        user_message = message.strip()
        print("agent running wait......")
        print("user_message:", user_message)
        print(session['messages'])

        session["messages"].append({"type":"user", "message":user_message})

        reply = agent.run_agent(user_message)
        session["messages"].append({"type":"ai", "message":reply})

        session.modified=True

        return redirect('/')

    except Exception:
        logger.exception("LangChain agent failed during /api/chat")
        return jsonify({"error": "The AI agent encountered an error. Please try again."}), 500
