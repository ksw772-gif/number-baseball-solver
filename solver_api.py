from flask import Flask, request, jsonify
from flask_cors import CORS
from solver_core import Solver
import uuid

app = Flask(__name__)
CORS(app)

sessions = {}

@app.route("/session", methods=["POST"])
def create_session():
    sid = str(uuid.uuid4())
    sessions[sid] = Solver()
    return jsonify({"session_id": sid})

@app.route("/session/<sid>/next_guess", methods=["GET"])
def next_guess(sid):
    solver = sessions.get(sid)
    if not solver:
        return jsonify({"error": "invalid session"}), 404
    return jsonify({"guess": solver.next_guess()})

@app.route("/session/<sid>/apply_hint", methods=["POST"])
def apply_hint(sid):
    solver = sessions.get(sid)
    if not solver:
        return jsonify({"error": "invalid session"}), 404

    data = request.json
    guess = data["guess"]
    hint_str = data["hint"]

    s = int(hint_str.split("ㅇ")[0]) if "ㅇ" in hint_str else 0
    b = int(hint_str.split("ㅌ")[0].split()[-1]) if "ㅌ" in hint_str else 0
    m = int(hint_str.split("ㅁ")[0].split()[-1]) if "ㅁ" in hint_str else 0

    solver.apply_hint(guess, (s, b, m))
    return jsonify({"remaining": len(solver.candidates)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
