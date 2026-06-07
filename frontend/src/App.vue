<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">📝 我的待办清单</h1>

      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">添加新任务</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <input
            v-model="newTask.title"
            type="text"
            placeholder="任务标题"
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
          <input
            v-model="newTask.content"
            type="text"
            placeholder="任务详情（可选）"
            class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            v-model="newTask.due_date"
            type="datetime-local"
            class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          @click="addTask"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors font-medium"
        >
          添加任务
        </button>
      </div>

      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">筛选和排序</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">分类筛选</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="cat in filterCategories"
                :key="cat"
                @click="filterCategory = cat"
                :class="[
                  'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
                  filterCategory === cat ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                {{ cat }}
              </button>
              <button
                @click="filterCategory = ''"
                :class="[
                  'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
                  !filterCategory ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                全部
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">完成状态</label>
            <div class="flex gap-2">
              <button
                @click="filterCompleted = ''"
                :class="[
                  'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
                  !filterCompleted ? 'bg-purple-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                全部
              </button>
              <button
                @click="filterCompleted = 'false'"
                :class="[
                  'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
                  filterCompleted === 'false' ? 'bg-purple-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                未完成
              </button>
              <button
                @click="filterCompleted = 'true'"
                :class="[
                  'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
                  filterCompleted === 'true' ? 'bg-purple-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                已完成
              </button>
            </div>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">排序方式</label>
          <div class="flex gap-2">
            <button
              @click="sortBy = 'created_at'"
              :class="[
                'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
                sortBy === 'created_at' ? 'bg-green-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              按创建时间
            </button>
            <button
              @click="sortBy = 'due_date'"
              :class="[
                'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
                sortBy === 'due_date' ? 'bg-green-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              按截止时间
            </button>
            <button
              @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
              class="px-3 py-1 rounded-lg text-sm font-medium bg-gray-200 text-gray-700 hover:bg-gray-300 transition-colors"
            >
              {{ sortOrder === 'asc' ? '升序 ↑' : '降序 ↓' }}
            </button>
          </div>
        </div>
      </div>

      <div class="space-y-4">
        <div
          v-for="task in filteredSortedTasks"
          :key="task.id"
          class="bg-white rounded-xl shadow-md p-5 hover:shadow-lg transition-shadow"
        >
          <div v-if="!editingTaskId || editingTaskId !== task.id" class="flex items-start gap-4">
            <button
              @click="toggleComplete(task)"
              :class="[
                'w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 mt-1',
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
              <div class="flex flex-wrap items-center gap-3 mt-2">
                <span
                  :class="[
                    'inline-block px-3 py-1 rounded-full text-xs font-medium',
                    getCategoryColor(task.category)
                  ]"
                >
                  {{ task.category }}
                </span>
                <span v-if="task.due_date" :class="[
                  'inline-block px-3 py-1 rounded-full text-xs font-medium',
                  getTimeStatusColor(task)
                ]">
                  {{ getTimeRemaining(task) }}
                </span>
                <span class="text-gray-400 text-xs">创建于: {{ formatDate(task.created_at) }}</span>
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
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <select
                v-model="editingTask.category"
                class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="工作">工作</option>
                <option value="学习">学习</option>
                <option value="生活">生活</option>
                <option value="其他">其他</option>
              </select>
              <input
                v-model="editingTask.due_date"
                type="datetime-local"
                class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
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

        <div v-if="filteredSortedTasks.length === 0" class="text-center py-12 text-gray-400">
          暂无任务，添加一个吧！
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const tasks = ref([])
const newTask = ref({
  title: '',
  content: '',
  category: '',
  due_date: ''
})
const filterCategory = ref('')
const filterCompleted = ref('')
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const editingTaskId = ref(null)
const editingTask = ref({
  title: '',
  content: '',
  category: '',
  due_date: ''
})
const now = ref(new Date())
let timer = null

const filterCategories = ['工作', '学习', '生活', '其他']

const filteredSortedTasks = computed(() => {
  let result = tasks.value.slice()

  // 分类筛选
  if (filterCategory.value) {
    result = result.filter(t => t.category === filterCategory.value)
  }

  // 完成状态筛选
  if (filterCompleted.value === 'true') {
    result = result.filter(t => t.completed)
  } else if (filterCompleted.value === 'false') {
    result = result.filter(t => !t.completed)
  }

  // 排序
  result.sort((a, b) => {
    let aVal, bVal
    if (sortBy.value === 'due_date') {
      aVal = a.due_date ? new Date(a.due_date) : new Date(0)
      bVal = b.due_date ? new Date(b.due_date) : new Date(0)
    } else {
      aVal = new Date(a.created_at)
      bVal = new Date(b.created_at)
    }

    if (sortOrder.value === 'asc') {
      return aVal - bVal
    } else {
      return bVal - aVal
    }
  })

  return result
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
      body: JSON.stringify({
        title: newTask.value.title,
        content: newTask.value.content,
        category: newTask.value.category,
        due_date: newTask.value.due_date || null
      })
    })
    const task = await res.json()
    tasks.value.unshift(task)
    newTask.value = { title: '', content: '', category: '', due_date: '' }
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
  editingTask.value = { 
    title: task.title, 
    content: task.content || '', 
    category: task.category,
    due_date: task.due_date || ''
  }
}

async function saveEdit() {
  try {
    const res = await fetch(`/api/tasks/${editingTaskId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: editingTask.value.title,
        content: editingTask.value.content,
        category: editingTask.value.category,
        due_date: editingTask.value.due_date || null
      })
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

function getTimeRemaining(task) {
  if (!task.due_date) return '无截止时间'
  
  const due = new Date(task.due_date)
  const diff = due - now.value
  
  if (task.completed) {
    return '已完成'
  }
  
  if (diff < 0) {
    return '已过期'
  }
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  if (days > 0) {
    return `还剩 ${days} 天 ${hours} 小时`
  } else if (hours > 0) {
    return `还剩 ${hours} 小时 ${minutes} 分钟`
  } else {
    return `还剩 ${minutes} 分钟`
  }
}

function getTimeStatusColor(task) {
  if (!task.due_date || task.completed) {
    return 'bg-gray-100 text-gray-700'
  }
  
  const due = new Date(task.due_date)
  const diff = due - now.value
  
  if (diff < 0) {
    return 'bg-red-100 text-red-800'
  } else if (diff < 24 * 60 * 60 * 1000) {
    return 'bg-orange-100 text-orange-800'
  } else {
    return 'bg-teal-100 text-teal-800'
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchTasks()
  timer = setInterval(() => {
    now.value = new Date()
  }, 60000) // 每分钟更新一次
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>
