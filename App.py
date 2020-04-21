from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskempleado'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes

##############################################################################################
                                       #empleados#
############################################################################################## 
@app.route('/')
def hm():
    return render_template('h.html')

@app.route('/add')
def add():
    return render_template('agre.html')

@app.route('/add_empleado', methods=['POST'])
def add_empleado():
    if request.method == 'POST':
        cargo = request.form['cargo']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        email= request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO empleados (cargo, nombre, apellido, cedula, telefono, email) VALUES (%s,%s,%s,%s,%s,%s)", (cargo, nombre, apellido, cedula, telefono, email))
        mysql.connection.commit()
        flash('Employye Added successfully')
        return redirect(url_for('add'))

@app.route('/emple')
def em_empleado():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados')
    data = cur.fetchall()
    cur.close()
    return render_template('emp.html', empleados = data)

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-empleado.html', empleado = data[0])


@app.route('/update/<id>', methods=['POST'])
def update_empleado(id):
    if request.method == 'POST':
        cargo = request.form['cargo']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE empleados
            SET cargo = %s,
                nombre = %s,
                apellido = %s,
                cedula = %s,
                telefono = %s,
                email = %s
            WHERE id = %s
        """, (cargo, nombre, apellido, cedula, telefono, email, id))
        mysql.connection.commit()
        return redirect(url_for('em_empleado'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empleados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('em_empleado'))

##############################################################################################
                                       #evaluacion#
##############################################################################################                                       
@app.route('/eva')
def eva():
    return render_template('h.html')

@app.route('/eva_empleado', methods=['POST'])
def eva_empleado():
    if request.method == 'POST':
        id = request.form['id']
        atencion = request.form['atencion']
        persona = request.form['persona']
        normas = request.form['normas']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO evaluacion (id, atencion, persona, normas) VALUES (%s,%s,%s,%s)", (id, atencion, persona, normas))
        mysql.connection.commit()
        flash('Employye Added successfully')
        return redirect(url_for('eva'))

@app.route('/eval')
def eval_empleado():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM evaluacion')
    data = cur.fetchall()
    cur.close()
    return render_template('eval.html', evaluacion = data)



@app.route('/deleteeva/<string:id>', methods = ['POST','GET'])
def delete_eva(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM evaluacion WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('eval_empleado'))

@app.route('/ev')
def ev():
    return render_template('ev.html')



#politicas

@app.route('/polit')
def polit():
    return render_template('poli.html')

# starting the app
if __name__ == "__main__":
    app.run(port=9000, debug=True)
