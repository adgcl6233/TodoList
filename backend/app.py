
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'todos.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            category TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    tasks = cursor.fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, content, category)
        VALUES (?, ?, ?)
    ''', (data['title'], data.get('content', ''), data['category']))
    conn.commit()
    task_id = cursor.lastrowid
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return jsonify(dict(task)), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if 'title' in data:
        updates.append('title = ?')
        params.append(data['title'])
    if 'content' in data:
        updates.append('content = ?')
        params.append(data['content'])
    if 'category' in data:
        updates.append('category = ?')
        params.append(data['category'])
    if 'completed' in data:
        updates.append('completed = ?')
        params.append(data['completed'])
    
    updates.append('updated_at = CURRENT_TIMESTAMP')
    params.append(task_id)
    
    cursor.execute(f'''
        UPDATE tasks 
        SET {', '.join(updates)}
        WHERE id = ?
    ''', params)
    
    conn.commit()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    
    if task:
        return jsonify(dict(task))
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
