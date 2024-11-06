from flask import Flask
from flask_cors import CORS
from flask import jsonify, request
import pymysql

app = Flask(__name__)  # Crea una instancia de la aplicación Flask

# Permite acceder desde una API externa
CORS(app)

# Función para conectarse a la base de datos MySQL
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

# Ruta para consulta general del baúl de contraseñas
@app.route("/")
def consulta_general():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM baul""")
        datos = cur.fetchall()
        data = []

        for row in datos:
            dato = {'id_baul': row[0], 'Plataforma': row[1], 'usuario': row[2], 'clave': row[3]}
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baúl de contraseñas'})
    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})
# Ruta para consulta individual de un registro en el baúl
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM baul where id_baul='{}'""".format(codigo))
        datos = cur.fetchone()

        cur.close()
        conn.close()
        # Aquí falta retornar los datos si se encuentran
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

@app.route("/registro/", methods=['POST'])
def registro():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute("""
            INSERT INTO baul (plataforma, usuario, clave)
            VALUES (%s, %s, %s)
        """, (request.json['plataforma'], request.json['usuario'], request.json['clave']))
        conn.commit()  # Para confirmar la inserción de la información
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute("""
            DELETE FROM baul WHERE id_baul=%s
        """, (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    try:
        # Conexión a la base de datos
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()

        # Consulta SQL para actualizar un registro
        x = cur.execute("""
            UPDATE baul
            SET plataforma=%(plataforma)s, usuario=%(usuario)s, clave=%(clave)s
            WHERE id_baul=%(id_baul)s
        """, {
            'plataforma': request.json['plataforma'],
            'usuario': request.json['usuario'],
            'clave': request.json['clave'],
            'id_baul': codigo
        })

        # Confirmar los cambios
        conn.commit()
        cur.close()
        conn.close()

        # Retornar un mensaje de éxito
        return jsonify({'mensaje': 'Registro Actualizado'})

    except Exception as ex:
        # Manejar excepciones
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
if __name__ == '__main__':
    app.run(debug=True)