import logging

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize CORS
CORS(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='todo')


try:
    # Create the database and tables
    with app.app_context():
        db.create_all()
        logging.info("Database and tables created successfully.")
except OperationalError as e:
    logging.error(f"Error creating tables: {e}")


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(content=data['content'], date=data.get('date'), status=data.get('status', 'todo'))
    db.session.add(new_task)
    db.session.commit()
    logging.info(f"Task added: {new_task.id} - {new_task.content}")
    return jsonify(
        {'id': new_task.id, 'content': new_task.content, 'date': new_task.date, 'status': new_task.status}), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    logging.info(f"Retrieved {len(tasks)} tasks.")
    return jsonify(
        [{'id': task.id, 'content': task.content, 'date': task.date, 'status': task.status} for task in tasks])


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = Task.query.get_or_404(id)
    task.content = data.get('content', task.content)
    task.date = data.get('date', task.date)
    task.status = data.get('status', task.status)
    db.session.commit()
    logging.info(f"Task updated: {id} - {task.content}")
    return jsonify({'id': task.id, 'content': task.content, 'date': task.date, 'status': task.status})


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    logging.info(f"Task deleted: {id}")
    return '', 204


if __name__ == '__main__':
    app.run()
