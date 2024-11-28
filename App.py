from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'libreria'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libros')
    dataLibros = cur.fetchall()
    cur.close()  # Cerrar el cursor después de usarlo
    return render_template('index.html', libros=dataLibros)

@app.route('/add_libro', methods=['POST'])
def add_libro():
    if request.method == 'POST':
        titulolib = request.form['titulolib']
        idautor = request.form['idautor']
        nomautor = request.form['nomautor']
        idedit = request.form['idedit']
        nomedit = request.form['nomedit']
        aniopubli = request.form['aniopubli']
        
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO libros 
            (titulo_libro, id_autor, nombre_autor, id_editorial, nombre_editorial, anio_publicacion)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (titulolib, idautor, nomautor, idedit, nomedit, aniopubli))
        
        mysql.connection.commit()
        cur.close()  # Cerrar el cursor después de usarlo
        flash('Libro Añadido Exitosamente!!')

        return redirect(url_for('Index'))

@app.route('/autores')
def get_autores():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM autores')
    dataAutores = cur.fetchall()
    cur.close()  # Cerrar el cursor después de usarlo
    return render_template('autores.html', autores=dataAutores)

@app.route('/editoriales')
def get_editoriales():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM editoriales')
    dataEditoriales = cur.fetchall()
    cur.close()  # Cerrar el cursor después de usarlo
    return render_template('editoriales.html', editoriales=dataEditoriales)

@app.route('/edit/<int:id>')
def get_libro(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libros WHERE id = %s', (id,))
    data = cur.fetchone()  # fetchone en lugar de fetchall, ya que es un solo registro
    cur.close()  # Cerrar el cursor después de usarlo
    if data:
        return render_template('edit-libro.html', libro=data)
    else:
        flash('Libro no encontrado')
        return redirect(url_for('Index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_libro(id):
    if request.method == 'POST':
        titulolib = request.form['titulolib']
        idautor = request.form['idautor']
        nomautor = request.form['nomautor']
        idedit = request.form['idedit']
        nomedit = request.form['nomedit']
        aniopubli = request.form['aniopubli']
        
        cur = mysql.connection.cursor()
        cur.execute(''' 
            UPDATE libros
            SET titulo_libro = %s,
                id_autor = %s,
                nombre_autor = %s,
                id_editorial = %s,
                nombre_editorial = %s,
                anio_publicacion = %s
            WHERE id = %s
        ''', (titulolib, idautor, nomautor, idedit, nomedit, aniopubli, id))
        
        mysql.connection.commit()
        cur.close()  # Cerrar el cursor después de usarlo
        flash('Libro Actualizado Exitosamente!!')
        return redirect(url_for('Index'))

@app.route('/delete/<int:id>')
def delete_libro(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM libros WHERE id = %s', (id,))
        mysql.connection.commit()
        cur.close()  # Cerrar el cursor después de usarlo
        flash('Libro Eliminado Exitosamente!!')
    except Exception as e:
        flash(f'Error al eliminar libro: {e}')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
