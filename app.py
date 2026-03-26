from flask import Flask,render_template,request
from database import conectar

#crear app del proyecto

app = Flask(__name__)

#crear la ruta principal

@app.route('/')
def principal():
    return render_template('index.html')

#crear la ruta para registrar usuarios

@app.route('/guardar_usuario', methods=['POST'])    
def guardar_usuario():

    usuario = request.form['txtusuario']
    password = request.form['txtcontraseña']
    rolusu = request.form['txtrol']
    documento = request.form['txtdocumento']

    #llamar a la conexion

    con = conectar()
    cursor = con.cursor()

    #creal el sql

    sql = "INSERT INTO usuarios (usuario, PASSWORD, rol, docuempleado) VALUES (%s, %s, %s, %s)"
    
    #ejecutar la sentencia sql

    cursor.execute(sql, (usuario, password, rolusu, documento))
    con.commit()

    return "Usuario guardado"

    #validar que exista el usuario

@app.route('/validar_usuario', methods=['POST'])    
def validar_usuario():

    sql = "SELECT * FROM usuarios WHERE usuario = %s AND PASSWORD = %s"
    usuario = request.form['txtusuario']
    password = request.form['txtcontraseña']   

    con = conectar()
    cursor = con.cursor()
    cursor.execute(sql, (usuario, password))
    resultado = cursor.fetchone()   
    
    if resultado:
        return "Usuario válido"
    else:
        return "Usuario o contraseña incorrectos"
    

if __name__== '__main__':
    app.run(debug=True)