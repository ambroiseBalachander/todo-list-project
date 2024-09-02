const API_BASE_URL = 'http://localhost:8000/tasks';

async function showError(message) {
    alert(message);
}

async function loadTasks() {
    try {
        const response = await fetch(API_BASE_URL);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const tasks = await response.json();

        tasks.forEach(task => {
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';
            taskItem.dataset.id = task.id; // Store the task ID
            taskItem.innerHTML = `
                <div class="task-content">
                    <p style="font-weight: 500;">${task.content}</p>
                    <p class="task-date">Due: ${task.date || 'Not set'}</p>
                </div>
                <button class="delete-btn" onclick="deleteTask(this)">✕</button>
            `;

            const list = document.getElementById(task.status); // Use task status to determine list
            if (list) {
                list.appendChild(taskItem);
            }
        });
    } catch (error) {
        console.error('Error loading tasks:', error);
        showError('Unable to load tasks. Please try again later.');
    }
}

async function addTask() {
    const taskInput = document.getElementById('taskInput');
    const taskDate = document.getElementById('taskDate');
    const todoList = document.getElementById('todo');

    if (taskInput.value.trim() !== '') {
        const task = {
            content: taskInput.value,
            date: taskDate.value || null,
            status: 'todo'
        };

        try {
            const response = await fetch(API_BASE_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(task)
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const newTask = await response.json();

            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';
            taskItem.dataset.id = newTask.id; // Store the task ID
            taskItem.innerHTML = `
                <div class="task-content">
                    <p style="font-weight: 500;">${newTask.content}</p>
                    <p class="task-date">Due: ${newTask.date || 'Not set'}</p>
                </div>
                <button class="delete-btn" onclick="deleteTask(this)">✕</button>
            `;
            todoList.appendChild(taskItem);

            taskInput.value = '';
            taskDate.value = '';
        } catch (error) {
            console.error('Error adding task:', error);
            showError('Unable to add task. Please try again later.');
        }
    }
}

async function deleteTask(button) {
    const taskItem = button.closest('.task-item');
    const taskId = taskItem.dataset.id;

    try {
        const response = await fetch(`${API_BASE_URL}/${taskId}`, { method: 'DELETE' });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        taskItem.remove();
    } catch (error) {
        console.error('Error deleting task:', error);
        showError('Unable to delete task. Please try again later.');
    }
}

async function updateTask(taskId, updatedTask) {
    try {
        const response = await fetch(`${API_BASE_URL}/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedTask)
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const updated = await response.json();
        return updated;
    } catch (error) {
        console.error('Error updating task:', error);
        showError('Unable to update task. Please try again later.');
    }
}

function triggerConfetti() {
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
    });
}

// Initialize Sortable for each list
const lists = document.querySelectorAll('.task-list');
lists.forEach(list => {
    new Sortable(list, {
        group: 'shared',
        animation: 150,
        onEnd: async function (evt) {
            const taskId = evt.item.dataset.id;
            const newStatus = evt.to.id; // Assume this is 'todo', 'doing', or 'finished'

            try {
                await updateTask(taskId, { status: newStatus });
                if (newStatus === 'finished') {
                    triggerConfetti();
                }
            } catch (error) {
                console.error('Error updating task status:', error);
                showError('Unable to update task status. Please try again later.');
            }
        }
    });
});

// Load tasks when the page is loaded
document.addEventListener('DOMContentLoaded', loadTasks);
