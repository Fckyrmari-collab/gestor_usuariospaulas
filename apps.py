from flask import Flask, render_template, url_for, request, redirect, flash, session
from database import conectar

apps = Flask(__name__)
apps.secret_key = "9877866554"

@apps.route("/")
def login():
     return render_template("login.html")

@apps.route('/login', methods=["POST"])
def login_form():

        user = request.form['txtusuario']
        password = request.form['txtcontraseña']

        con = conectar()
        cursor = con.cursor()

        sql = "SELECT * FROM usuarios WHERE usuario=%s AND PASSWORD=%s"
        cursor.execute(sql,(user,password))
        
        #resultado de la consulta
        user = cursor.fetchone()

        if user:

            #guardar las variables de sesion

            session['usuario'] = user[1]
            session['rol'] = user[3]

            #if rol == rol:

            if user[3] == "administrador":
                        return render_template('index.html')
            
            elif user[3] == 'empleado':
                        return render_template('index.html')
        else:
                flash("Usuario o contraseña incorrecta", "danger")
                return redirect(url_for('login'))
        
#validar sesion en la pagina incial 

@apps.route('/inicio')
def inicio():
        
        if 'usuario' not in session:
                return redirect(url_for('login'))
        else:
                render_template('index.html')

#cerrar la sesion
@apps.route('/salir')
def salir():
        session.clear()
        return redirect(url_for('login'))
                                
if __name__ == '__main__':
    apps.run(debug=True) 