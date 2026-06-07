
&lt;template&gt;
  &lt;div class="min-h-screen bg-gray-50 py-8 px-4"&gt;
    &lt;div class="max-w-4xl mx-auto"&gt;
      &lt;h1 class="text-3xl font-bold text-gray-800 mb-8 text-center"&gt;📝 我的待办清单&lt;/h1&gt;

      &lt;div class="bg-white rounded-xl shadow-lg p-6 mb-6"&gt;
        &lt;h2 class="text-lg font-semibold text-gray-700 mb-4"&gt;添加新任务&lt;/h2&gt;
        &lt;div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4"&gt;
          &lt;input
            v-model="newTask.title"
            type="text"
            placeholder="任务标题"
            class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          /&gt;
          &lt;input
            v-model="newTask.content"
            type="text"
            placeholder="任务详情（可选）"
            class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          /&gt;
          &lt;select
            v-model="newTask.category"
            class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          &gt;
            &lt;option value=""&gt;选择分类&lt;/option&gt;
            &lt;option value="工作"&gt;工作&lt;/option&gt;
            &lt;option value="学习"&gt;学习&lt;/option&gt;
            &lt;option value="生活"&gt;生活&lt;/option&gt;
            &lt;option value="其他"&gt;其他&lt;/option&gt;
          &lt;/select&gt;
        &lt;/div&gt;
        &lt;button
          @click="addTask"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors font-medium"
        &gt;
          添加任务
        &lt;/button&gt;
      &lt;/div&gt;

      &lt;div class="bg-white rounded-xl shadow-lg p-6 mb-6"&gt;
        &lt;h2 class="text-lg font-semibold text-gray-700 mb-4"&gt;筛选任务&lt;/h2&gt;
        &lt;div class="flex flex-wrap gap-3"&gt;
          &lt;button
            v-for="cat in filterCategories"
            :key="cat"
            @click="filterCategory = cat"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              filterCategory === cat ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          &gt;
            {{ cat }}
          &lt;/button&gt;
          &lt;button
            @click="filterCategory = ''"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              !filterCategory ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          &gt;
            全部
          &lt;/button&gt;
        &lt;/div&gt;
      &lt;/div&gt;

      &lt;div class="space-y-4"&gt;
        &lt;div
          v-for="task in filteredTasks"
          :key="task.id"
          class="bg-white rounded-xl shadow-md p-5 hover:shadow-lg transition-shadow"
        &gt;
          &lt;div v-if="!editingTaskId || editingTaskId !== task.id" class="flex items-start gap-4"&gt;
            &lt;button
              @click="toggleComplete(task)"
              :class="[
                'w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0',
                task.completed ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-blue-500'
              ]"
            &gt;
              &lt;span v-if="task.completed" class="text-white text-sm"&gt;✓&lt;/span&gt;
            &lt;/button&gt;
            &lt;div class="flex-1"&gt;
              &lt;h3
                :class="[
                  'text-lg font-medium',
                  task.completed ? 'text-gray-400 line-through' : 'text-gray-800'
                ]"
              &gt;
                {{ task.title }}
              &lt;/h3&gt;
              &lt;p v-if="task.content" class="text-gray-500 text-sm mt-1"&gt;{{ task.content }}&lt;/p&gt;
              &lt;div class="flex items-center gap-3 mt-2"&gt;
                &lt;span
                  :class="[
                    'inline-block px-3 py-1 rounded-full text-xs font-medium',
                    getCategoryColor(task.category)
                  ]"
                &gt;
                  {{ task.category }}
                &lt;/span&gt;
                &lt;span class="text-gray-400 text-xs"&gt;{{ formatDate(task.created_at) }}&lt;/span&gt;
              &lt;/div&gt;
            &lt;/div&gt;
            &lt;div class="flex gap-2"&gt;
              &lt;button
                @click="startEdit(task)"
                class="text-blue-500 hover:text-blue-700 p-2"
              &gt;
                ✏️
              &lt;/button&gt;
              &lt;button
                @click="deleteTask(task.id)"
                class="text-red-500 hover:text-red-700 p-2"
              &gt;
                🗑️
              &lt;/button&gt;
            &lt;/div&gt;
          &lt;/div&gt;

          &lt;div v-else class="space-y-4"&gt;
            &lt;input
              v-model="editingTask.title"
              type="text"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            /&gt;
            &lt;input
              v-model="editingTask.content"
              type="text"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            /&gt;
            &lt;select
              v-model="editingTask.category"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            &gt;
              &lt;option value="工作"&gt;工作&lt;/option&gt;
              &lt;option value="学习"&gt;学习&lt;/option&gt;
              &lt;option value="生活"&gt;生活&lt;/option&gt;
              &lt;option value="其他"&gt;其他&lt;/option&gt;
            &lt;/select&gt;
            &lt;div class="flex gap-3"&gt;
              &lt;button
                @click="saveEdit"
                class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors"
              &gt;
                保存
              &lt;/button&gt;
              &lt;button
                @click="cancelEdit"
                class="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition-colors"
              &gt;
                取消
              &lt;/button&gt;
            &lt;/div&gt;
          &lt;/div&gt;
        &lt;/div&gt;

        &lt;div v-if="filteredTasks.length === 0" class="text-center py-12 text-gray-400"&gt;
          暂无任务，添加一个吧！
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup&gt;
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

const filteredTasks = computed(() =&gt; {
  if (!filterCategory.value) return tasks.value
  return tasks.value.filter(t =&gt; t.category === filterCategory.value)
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
    const index = tasks.value.findIndex(t =&gt; t.id === task.id)
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
    const index = tasks.value.findIndex(t =&gt; t.id === editingTaskId.value)
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
    tasks.value = tasks.value.filter(t =&gt; t.id !== id)
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

onMounted(() =&gt; {
  fetchTasks()
})
&lt;/script&gt;
