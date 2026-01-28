// DOM Elements
const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const taskList = document.getElementById('task-list');
const taskCount = document.getElementById('task-count');
const clearCompletedBtn = document.getElementById('clear-completed');
const filterBtns = document.querySelectorAll('.filter-btn');

// State
let tasks = [];
let currentFilter = 'all';

// API Functions
async function fetchTasks() {
  try {
    const response = await fetch('/api/tasks');
    tasks = await response.json();
    renderTasks();
  } catch (error) {
    console.error('Error fetching tasks:', error);
  }
}

async function createTask(title) {
  try {
    const response = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    });
    const newTask = await response.json();
    tasks.push(newTask);
    renderTasks();
  } catch (error) {
    console.error('Error creating task:', error);
  }
}

async function updateTask(id, updates) {
  try {
    const response = await fetch(`/api/tasks/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
    const updatedTask = await response.json();
    const index = tasks.findIndex(t => t.id === id);
    if (index !== -1) {
      tasks[index] = updatedTask;
    }
    renderTasks();
  } catch (error) {
    console.error('Error updating task:', error);
  }
}

async function deleteTask(id) {
  try {
    await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
    tasks = tasks.filter(t => t.id !== id);
    renderTasks();
  } catch (error) {
    console.error('Error deleting task:', error);
  }
}

// Render Functions
function renderTasks() {
  const filteredTasks = tasks.filter(task => {
    if (currentFilter === 'active') return !task.completed;
    if (currentFilter === 'completed') return task.completed;
    return true;
  });

  if (filteredTasks.length === 0) {
    taskList.innerHTML = `
      <li class="empty-state">
        ${currentFilter === 'all' ? 'No tasks yet. Add one above!' : `No ${currentFilter} tasks.`}
      </li>
    `;
  } else {
    taskList.innerHTML = filteredTasks.map(task => `
      <li class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
        <div class="task-checkbox ${task.completed ? 'checked' : ''}" onclick="toggleTask('${task.id}')"></div>
        <span class="task-title">${escapeHtml(task.title)}</span>
        <button class="task-delete" onclick="deleteTask('${task.id}')">&times;</button>
      </li>
    `).join('');
  }

  updateStats();
}

function updateStats() {
  const activeTasks = tasks.filter(t => !t.completed).length;
  const totalTasks = tasks.length;
  taskCount.textContent = `${activeTasks} of ${totalTasks} task${totalTasks !== 1 ? 's' : ''} remaining`;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Event Handlers
function toggleTask(id) {
  const task = tasks.find(t => t.id === id);
  if (task) {
    updateTask(id, { completed: !task.completed });
  }
}

taskForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const title = taskInput.value.trim();
  if (title) {
    createTask(title);
    taskInput.value = '';
  }
});

clearCompletedBtn.addEventListener('click', async () => {
  const completedTasks = tasks.filter(t => t.completed);
  for (const task of completedTasks) {
    await deleteTask(task.id);
  }
});

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderTasks();
  });
});

// Initialize
fetchTasks();
