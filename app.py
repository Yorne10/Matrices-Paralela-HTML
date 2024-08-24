# gui.py
from flask import Flask, render_template, request, redirect, url_for
from database import create_connection, save_matrix, get_matrices
import threading
import webbrowser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    rows = None
    cols = None
    if request.method == 'POST':
        rows = int(request.form.get('rows'))
        cols = int(request.form.get('cols'))

    return render_template('index.html', rows=rows, cols=cols)

@app.route('/save_matrix', methods=['POST'])
def save_matrix_route():
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])
    matrix = []

    for i in range(rows):
        row = []
        for j in range(cols):
            cell_value = request.form.get(f'cell_{i}_{j}')
            row.append(cell_value)
        matrix.append(row)

    save_matrix_to_db(matrix)
    return redirect(url_for('index'))

@app.route('/matrices')
def show_matrices():
    conn = create_connection()
    matrices = get_matrices(conn)
    conn.close()
    return render_template('matrices.html', matrices=matrices)

def save_matrix_to_db(matrix):
    conn = create_connection()
    save_matrix(conn, str(matrix))
    conn.close()

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)



