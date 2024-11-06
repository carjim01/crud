from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import os

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Permite acceder desde una API externa
CORS(app)

# Cargar variables de entorno (credenciales de la base de datos)
""" DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = os.getenv('DB_NAME', 'gestor_contrasena') """

# Función para conectarse a la base de datos MySQL
def conectar():
        conn = pymysql.connect(
            host='localhost',
            user= 'carlos',
            passwd='12345',
            db='gestor_contrasena',
            charset='utf8mb4'
        )
        return conn
    

# Ruta para consulta general del baúl de contraseñas
@app.route("/", methods=['GET'])
def consulta_general():
    try:
        conn = conectar()
       # if conn is None:
         #   return jsonify({'mensaje': 'Error al conectar a la base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul")
        datos = cur.fetchall()
        data = []

        for row in datos:
            dato = {'id_baul': row[0], 'Plataforma': row[1], 'usuario': row[2], 'clave': row[3]}
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baúl de contraseñas'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'}), 500

# Ruta para consulta individual de un registro en el baúl
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar()
        if conn is None:
            return jsonify({'mensaje': 'Error al conectar a la base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul WHERE id_baul=%s", (codigo,))
        datos = cur.fetchone()

        cur.close()
        conn.close()

        if datos:
            dato = {'id_baul': datos[0], 'Plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}
            return jsonify({'baul': dato, 'mensaje': 'Consulta exitosa'})
        else:
            return jsonify({'mensaje': 'Registro no encontrado'}), 404
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'}), 500

# Ruta para registrar un nuevo dato en el baúl
@app.route("/registro/", methods=['POST'])
def registro():
    try:
        conn = conectar()
        if conn is None:
            return jsonify({'mensaje': 'Error al conectar a la base de datos'}), 500

        cur = conn.cursor()

        # Validar que los datos existan
        plataforma = request.json.get('plataforma')
        usuario = request.json.get('usuario')
        clave = request.json.get('clave')

        if not plataforma or not usuario or not clave:
            return jsonify({'mensaje': 'Faltan datos'}), 400

        cur.execute("""
            INSERT INTO baul (plataforma, usuario, clave)
            VALUES (%s, %s, %s)
        """, (plataforma, usuario, clave))
        conn.commit()

        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'}), 201
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'}), 500

# Ruta para eliminar un registro del baúl
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar()
        if conn is None:
            return jsonify({'mensaje': 'Error al conectar a la base de datos'}), 500

        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul=%s", (codigo,))
        conn.commit()

        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro eliminado'}), 200
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'}), 500

# Ruta para actualizar un registro en el baúl
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    try:
        conn = conectar()
        if conn is None:
            return jsonify({'mensaje': 'Error al conectar a la base de datos'}), 500

        cur = conn.cursor()

        # Validar que los datos existan
        plataforma = request.json.get('plataforma')
        usuario = request.json.get('usuario')
        clave = request.json.get('clave')

        if not plataforma or not usuario or not clave:
            return jsonify({'mensaje': 'Faltan datos'}), 400

        cur.execute("""
            UPDATE baul
            SET plataforma=%s, usuario=%s, clave=%s
            WHERE id_baul=%s
        """, (plataforma, usuario, clave, codigo))
        conn.commit()

        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro actualizado'}), 200
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'}), 500

if __name__ == "__main__":
    app.run(debug=True)
