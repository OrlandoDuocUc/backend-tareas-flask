from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar CORS para permitir múltiples orígenes
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:8000", 
    "http://127.0.0.1:8000",
    "http://localhost:5500",
    "https://taskmaster-render-supabase-orlando.netlify.app"  # ← AGREGAR ESTA LÍNEA
])

# Configuración de Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Ruta raíz
@app.route('/')
def home():
    return jsonify({
        "message": "API de Tareas funcionando correctamente",
        "endpoints": {
            "GET /tasks": "Obtener todas las tareas",
            "POST /tasks": "Crear nueva tarea",
            "PUT /tasks/<id>": "Actualizar tarea",
            "DELETE /tasks/<id>": "Eliminar tarea"
        }
    })

# Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        response = supabase.table('tasks').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('description'):
            return jsonify({"error": "Título y descripción son requeridos"}), 400
        
        response = supabase.table('tasks').insert({
            'title': data['title'],
            'description': data['description']
        }).execute()
        
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar tarea
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400
        
        response = supabase.table('tasks').update(data).eq('id', task_id).execute()
        
        if not response.data:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        response = supabase.table('tasks').delete().eq('id', task_id).execute()
        
        if not response.data:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)