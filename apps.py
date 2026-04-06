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
                        return redirect(url_for("inicio"))

            elif user[3] == "empleado":
                        return render_template('empleado.html')

        else:
            flash("Usuario o contraseña incorrecta")
            return redirect(url_for('login'))
    
#validar sesion en la pagina incial 

               
#ruta para listar 
@apps.route('/inicio')
def inicio():
    # Validar que la sesión esté activa
    if 'usuario' not in session:
        return redirect(url_for('inicio'))
    
    con = conectar()
    cursor = con.cursor()
    
    # Consultar todos los usuarios
    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    usuarios_registrados = cursor.fetchall()
    
    cursor.close()
    con.close()
    
    return render_template('usuarios.html', user=usuarios_registrados)

#cerrar la sesion
@apps.route('/salir')
def salir():
        session.clear()
        return redirect(url_for('login'))
    
# RUTA PARA ELIMINAR LOS USUARIOS TIPO EMPLEADO
@apps.route('/eliminar/<int:id>')
def eliminarusu(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    con = conectar()
    cursor = con.cursor()
    
    # PASO 1: Primero buscamos al usuario para ver su rol
    cursor.execute("SELECT rol FROM usuarios WHERE id_usuarios = %s", (id,))
    usuario = cursor.fetchone()
    
    if usuario:
        rol = usuario[0]
        
        # PASO 2: Validar que no sea administrador
        if rol == "administrador":
            flash("No se puede eliminar un usuario administrador", "danger")
        else:
            # PASO 3: Si es empleado, lo borramos
            sql_delete = "DELETE FROM usuarios WHERE id_usuarios = %s"
            cursor.execute(sql_delete, (id,))
            con.commit()
            flash("Usuario eliminado correctamente", "success")
    else:
        flash("Usuario no encontrado", "warning")
            
    cursor.close()
    con.close()
    return redirect(url_for('lista_usuarios')) # Debes retornar a la tabla
                                
if __name__ == '__main__':
    apps.run(debug=True) 