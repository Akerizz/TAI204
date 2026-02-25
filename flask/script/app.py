from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URL base de tu FastAPI en Docker
API_URL = "http://localhost:8008/v1"

@app.route("/")
def index():
    # Obtener todos los usuarios (GET)
    try:
        respuesta = requests.get(f"{API_URL}/Usuarios/")
        datos = respuesta.json()
        usuarios = datos.get("Usuarios", [])
    except Exception as e:
        print(f"Error conectando a la API: {e}")
        usuarios = []
        
    return render_template("index.html", usuarios=usuarios)

@app.route("/agregar", methods=["POST"])
def agregar():
    # Capturamos los datos del formulario HTML
    nuevo_usuario = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }
    # Enviamos el POST a FastAPI
    requests.post(f"{API_URL}/ParametroOP/", json=nuevo_usuario)
    return redirect(url_for("index"))

@app.route("/actualizar/<int:id_usuario>", methods=["POST"])
def actualizar(id_usuario):
    # Capturamos los nuevos datos del formulario
    usuario_actualizado = {
        "id": int(request.form["nuevo_id"]),
        "nombre": request.form["nuevo_nombre"],
        "edad": int(request.form["nueva_edad"])
    }
    # Enviamos el PUT a FastAPI (usando params porque configuraste el id como opcional en la URL)
    requests.put(f"{API_URL}/usuario/", params={"id": id_usuario}, json=usuario_actualizado)
    return redirect(url_for("index"))

@app.route("/eliminar/<int:id_usuario>", methods=["POST"])
def eliminar(id_usuario):
    # Enviamos el DELETE a FastAPI (usando params por el id opcional)
    requests.delete(f"{API_URL}/usuario/", params={"id": id_usuario})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5005)

    #.venv/Scripts/Activat