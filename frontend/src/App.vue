<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">📝 我的待办清单</h1>

      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">添加新任务</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <input
            v-model="newTask.title"
            type="text"
            placeholder="任务标题"
            class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            v-model="newTask.content"
            type="text"
            placeholder="任务详情（可选）"
            class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            v-model="newTask.category"
            class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">选择分类</option>
            <option value="工作">工作</option>
            <option value="学习">学习</option>
            <option value="生活">生活</option>
            <option value="其他">其他</option>
          </select>
        </div>
        <button
          @click="addTask"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors font-medium"
        >
          添加任务
        </button>
      </div>

      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">筛选任务</h2>
        <div class="flex flex-wrap gap-3">
          <button
            v-for="cat in filterCategories"
            :key="cat"
            @click="filterCategory = cat"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              filterCategory === cat ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            {{ cat }}
          </button>
          <button
            @click="filterCategory = ''"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              !filterCategory ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            全部
          </button>
        </div>
      </div>

      <div class="space-y-4">
        <div
          v-for="task in filteredTasks"
          :key="task.id"
          class="bg-white rounded-xl shadow-md p-5 hover:shadow-lg transition-shadow"
        >
          <div v-if="!editingTaskId || editingTaskId !== task.id" class="flex items-start gap-4">
            <button
              @click="toggleComplete(task)"
              :class="[
                'w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0',
                task.completed ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-blue-500'
              ]"
            >
              <span v-if="task.completed" class="text-white text-sm">✓</span>
            </button>
            <div class="flex-1">
              <h3
                :class="[
                  'text-lg font-medium',
                  task.completed ? 'text-gray-400 line-through' : 'text-gray-800'
                ]"
              >
                {{ task.title }}
              </h3>
              <p v-if="task.content" class="text-gray-500 text-sm mt-1">{{ task.content }}</p>
              <div class="flex items-center gap-3 mt-2">
                <span
                  :class="[
                    'inline-block px-3 py-1 rounded-full text-xs font-medium',
                    getCategoryColor(task.category)
                  ]"
                >
                  {{ task.category }}
                </span>
                <span class="text-gray-400 text-xs">{{ formatDate(task.created_at) }}</span>
              </div>
            </div>
            <div class="flex gap-2">
              <button
                @click="startEdit(task)"
                class="text-blue-500 hover:text-blue-700 p-2"
              >
                ✏️
              </button>
              <button
                @click="deleteTask(task.id)"
                class="text-red-500 hover:text-red-700 p-2"
              >
                🗑️
              </button>
            </div>
          </div>

          <div v-else class="space-y-4">
            <input
              v-model="editingTask.title"
              type="text"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              v-model="editingTask.content"
              type="text"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <select
              v-model="editingTask.category"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="工作">工作</option>
              <option value="学习">学习</option>
              <option value="生活">生活</option>
              <option value="其他">其他</option>
            </select>
            <div class="flex gap-3">
              <button
                @click="saveEdit"
                class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors"
              >
                保存
              </button>
              <button
                @click="cancelEdit"
                class="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition-colors"
              >
                取消
              </button>
            </div>
          </div>
        </div>

        <div v-if="filteredTasks.length === 0" class="text-center py-12 text-gray-400">
          暂无任务，添加一个吧！
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const tasks = ref([])
const newTask = ref({
  title: '',
  content: '',
  category: ''
})
const filterCategory = ref('')
const editingTaskId = ref(null)
const editingTask = ref({
  title: '',
  content: '',
  category: ''
})

const filterCategories = ['工作', '学习', '生活', '其他']

const filteredTasks = computed(() => {
  if (!filterCategory.value) return tasks.value
  return tasks.value.filter(t => t.category === filterCategory.value)
})

async function fetchTasks() {
  try {
    const res = await fetch('/api/tasks')
    tasks.value = await res.json()
  } catch (error) {
    console.error('获取任务失败:', error)
  }
}

async function addTask() {
  if (!newTask.value.title || !newTask.value.category) {
    alert('请填写任务标题和分类！')
    return
  }
  
  try {
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTask.value)
    })
    const task = await res.json()
    tasks.value.unshift(task)
    newTask.value = { title: '', content: '', category: '' }
  } catch (error) {
    console.error('添加任务失败:', error)
  }
}

async function toggleComplete(task) {
  try {
    const res = await fetch(`/api/tasks/${task.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: !task.completed })
    })
    const updated = await res.json()
    const index = tasks.value.findIndex(t => t.id === task.id)
    if (index !== -1) {
      tasks.value[index] = updated
    }
  } catch (error) {
    console.error('更新任务失败:', error)
  }
}

function startEdit(task) {
  editingTaskId.value = task.id
  editingTask.value = { ...task }
}

async function saveEdit() {
  try {
    const res = await fetch(`/api/tasks/${editingTaskId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingTask.value)
    })
    const updated = await res.json()
    const index = tasks.value.findIndex(t => t.id === editingTaskId.value)
    if (index !== -1) {
      tasks.value[index] = updated
    }
    editingTaskId.value = null
  } catch (error) {
    console.error('保存失败:', error)
  }
}

function cancelEdit() {
  editingTaskId.value = null
}

async function deleteTask(id) {
  if (!confirm('确定要删除这个任务吗？')) return
  
  try {
    await fetch(`/api/tasks/${id}`, {
      method: 'DELETE'
    })
    tasks.value = tasks.value.filter(t => t.id !== id)
  } catch (error) {
    console.error('删除任务失败:', error)
  }
}

function getCategoryColor(category) {
  const colors = {
    '工作': 'bg-blue-100 text-blue-800',
    '学习': 'bg-green-100 text-green-800',
    '生活': 'bg-yellow-100 text-yellow-800',
    '其他': 'bg-gray-100 text-gray-800'
  }
  return colors[category] || 'bg-gray-100 text-gray-800'
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchTasks()
})
</script>