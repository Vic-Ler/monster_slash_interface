from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# --- In-Memory Game State ---
game_data = {
    "current_round": 1,
    "rounds": {}
}


@app.route("/")
def index():
    return "Server läuft! /player für Spieler, /admin für Admin."


# --- Player Interface ---
@app.route("/player")
def player():
    return render_template("player.html")


# --- Admin Interface ---
@app.route("/admin")
def admin():
    return render_template("admin.html")


# --- API: Spieleraktion speichern ---
@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.json
    round_nr = game_data["current_round"]

    if round_nr not in game_data["rounds"]:
        game_data["rounds"][round_nr] = []

    game_data["rounds"][round_nr].append({
        "player": data["player"],
        "weapon": data["weapon"],
        "monster": data["monster"],
        "hp": int(data["hp"])
    })

    return jsonify({"status": "ok", "round": round_nr})


# --- API: Daten für Admin abrufen ---
@app.route("/api/round/<int:round_nr>")
def get_round(round_nr):
    if round_nr not in game_data["rounds"]:
        return jsonify([])

    # Sortierung: HP desc, bei Gleichstand random
    players = game_data["rounds"][round_nr][:]
    random.shuffle(players)
    players.sort(key=lambda x: x["hp"], reverse=True)
    return jsonify(players)


# --- API: Runde abschließen ---
@app.route("/api/close_round", methods=["POST"])
def close_round():
    game_data["current_round"] += 1
    return jsonify({"status": "round_closed", "new_round": game_data["current_round"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
