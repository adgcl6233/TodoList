
# 待办清单应用

一个简洁的Web待办清单应用，使用Vue3 + Flask + SQLite构建。

## 功能特性

- ✅ 增删改查任务
- ✅ 标记任务完成/未完成
- ✅ 按分类筛选（工作、学习、生活、其他）
- ✅ SQLite持久化存储
- ✅ 响应式设计

## 快速启动

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端将在 http://localhost:5000 启动

### 前端启动

打开新的终端：

```bash
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:3000 启动

## 技术栈

- 前端：Vue 3 + Vite + Tailwind CSS
- 后端：Python Flask
- 数据库：SQLite
