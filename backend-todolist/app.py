import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Configure SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize CORS
CORS(app)


# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(50))
    status = db.Column(db.String(50), default='todo')

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'date': self.date,
            'status': self.status
        }


# Create database tables
with app.app_context():
    db.create_all()


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(
        content=data['content'],
        date=data.get('date'),
        status=data.get('status', 'todo')
    )
    try:
        db.session.add(new_task)
        db.session.commit()
        logging.info(f"Task added: {new_task.id} - {new_task.content}")
        return jsonify(new_task.to_dict()), 201
    except SQLAlchemyError as e:
        logging.error(f"Error adding task: {e}")
        return jsonify({'error': 'Error adding task'}), 500


@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.all()
        logging.info(f"Retrieved {len(tasks)} tasks.")
        return jsonify([task.to_dict() for task in tasks])
    except SQLAlchemyError as e:
        logging.error(f"Error retrieving tasks: {e}")
        return jsonify({'error': 'Error retrieving tasks'}), 500


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = Task.query.get_or_404(id)
    try:
        task.content = data.get('content', task.content)
        task.date = data.get('date', task.date)
        task.status = data.get('status', task.status)
        db.session.commit()
        logging.info(f"Task updated: {task.id} - {task.content}")
        return jsonify(task.to_dict())
    except SQLAlchemyError as e:
        logging.error(f"Error updating task: {e}")
        return jsonify({'error': 'Error updating task'}), 500


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        logging.info(f"Task deleted: {task.id}")
        return '', 204
    except SQLAlchemyError as e:
        logging.error(f"Error deleting task: {e}")
        return jsonify({'error': 'Error deleting task'}), 500


if __name__ == '__main__':
    app.run()
