from project.backend.src.db.db_app import app


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    ...