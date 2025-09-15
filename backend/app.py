from flask import Flask, request, render_template, jsonify
import os
import requests
import json

app = Flask(__name__, static_folder='static', template_folder='templates')

# 🔹 Configuración de IBM Event Notifications
API_KEY = "IS7kdv370c5tj0JZZIhhc8pWmE6990x6saLNkTAmReYw"          # tu API key
INSTANCE_ID = "ecfbfb24-71c4-487d-9e31-1e230f71eae1"             # tu ID de instancia
TOPIC_ID = "ecfbfb24-71c4-487d-9e31-1e230f71eae1"                # tu ID de topic
ENDPOINT = "https://us-south.event-notifications.cloud.ibm.com" # según tu región

# 🔹 Almacenamiento de notas en memoria
notas = []

# 🔹 Función para enviar notificación
def send_notification(message):
    url = f"{ENDPOINT}/event-notifications/v1/instances/{INSTANCE_ID}/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "messages": [
            {
                "severity": "NORMAL",
                "shortDescription": "Evento desde Flask",
                "longDescription": message,
                "topicId": TOPIC_ID
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 202:
            print("✅ Notificación enviada correctamente")
        else:
            print("⚠️ Error al enviar notificación:", response.text)
    except Exception as e:
        print("⚠️ Excepción al enviar notificación:", str(e))

# 🔹 Rutas de Flask
@app.route('/')
def index():
    # Muestra todas las notas
    return render_template('index.html', notas=notas)

@app.route('/api/message')
def message():
    return jsonify({"message": "¡Hola mundo!"})

# 🔹 Endpoint para agregar una nota vía POST
@app.route('/api/nota', methods=['POST'])
def agregar_nota():
    data = request.json
    if 'titulo' in data and 'contenido' in data:
        nota = {
            "titulo": data['titulo'],
            "contenido": data['contenido']
        }
        notas.append(nota)
        # Enviar notificación a IBM Event Notifications
        send_notification(f"Se agregó una nueva nota: {data['titulo']}")
        return jsonify({"status": "ok", "nota": nota}), 201
    else:
        return jsonify({"status": "error", "message": "Datos incompletos"}), 400

# 🔹 Endpoint para recibir eventos de IBM Event Notifications
@app.route('/eventos', methods=['POST'])
def recibir_evento():
    evento = request.json
    print("Evento recibido:", json.dumps(evento, indent=2))
    # Ejemplo: si el evento tiene un mensaje de nota, lo guardamos
    if 'nota' in evento:
        notas.append(evento['nota'])
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
