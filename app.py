import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "tasks"

app = Flask(__name__)

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}


# Obtener todas las tareas
@app.route("/tasks", methods=["GET"])
def get_tasks():
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?select=*"
    response = requests.get(url, headers=headers)
    return jsonify(response.json()), response.status_code

# Crear una nueva tarea
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if not data.get("title") or not data.get("description"):
        return jsonify({"error": "title y description son obligatorios"}), 400
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    payload = [{
        "title": data["title"],
        "description": data["description"]
    }]
    response = requests.post(url, headers=headers, json=payload)
    try:
        return jsonify(response.json()), response.status_code
    except Exception:
        return jsonify({"response": response.text}), response.status_code

# Actualizar una tarea
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    if not data.get("title") or not data.get("description"):
        return jsonify({"error": "title y description son obligatorios"}), 400
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{task_id}"
    payload = {
        "title": data["title"],
        "description": data["description"]
    }
    response = requests.patch(url, headers=headers, json=payload)
    try:
        return jsonify(response.json()), response.status_code
    except Exception:
        return jsonify({"response": response.text}), response.status_code

# Eliminar una tarea
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{task_id}"
    response = requests.delete(url, headers=headers)
    try:
        return jsonify(response.json()), response.status_code
    except Exception:
        return jsonify({"response": response.text}), response.status_code

# Esta es la parte que faltaba - iniciar el servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)