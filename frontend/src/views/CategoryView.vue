<template>
  <div class="category-container">
    <el-header height="60px" class="header">
      <div class="header-content">
        <h1 class="logo">校园二手书交易平台</h1>
        <div class="header-right">
          <el-button type="primary" @click="goToHome">首页</el-button>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <div class="category-title">
        <h2>{{ categoryName }}</h2>
      </div>
      
      <div class="book-list">
        <el-card v-for="book in books" :key="book.id" class="book-card">
          <template #header>
            <div class="book-card-header">
              <h3>{{ book.title }}</h3>
              <span class="book-price">¥{{ book.price }}</span>
            </div>
          </template>
          <div class="book-card-body">
            <div class="book-image">
              <img :src="book.images[0] || 'https://via.placeholder.com/100'" alt="书籍封面" />
            </div>
            <div class="book-info">
              <p>作者: {{ book.author }}</p>
              <p>分类: {{ book.category }}</p>
              <p>成色: {{ book.condition }}</p>
              <p>交易方式: {{ book.delivery_type }}</p>
            </div>
          </div>
          <template #footer>
            <div class="book-card-footer">
              <el-button type="primary" @click="goToBookDetail(book.id)">查看详情</el-button>
            </div>
          </template>
        </el-card>
      </div>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-main>
    
    <el-footer height="60px" class="footer">
      <p>© 2026 校园二手书交易平台</p>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const categoryType = ref(route.params.type)
const books = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 计算分类名称
const categoryName = computed(() => {
  const categoryMap = {
    'all': '全部书籍',
    '教材': '教材',
    '教辅': '教辅',
    '文学': '文学',
    '科技': '科技',
    '其他': '其他'
  }
  return categoryMap[categoryType.value] || '全部书籍'
})

// 获取分类书籍列表
const getCategoryBooks = async () => {
  try {
    const category = categoryType.value === 'all' ? '' : categoryType.value
    const response = await fetch(`/api/books?page=${currentPage.value}&per_page=${pageSize.value}&category=${category}`)
    const data = await response.json()
    if (data.code === 200) {
      books.value = data.books
      total.value = data.total
    }
  } catch (error) {
    console.error('获取分类书籍列表失败:', error)
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  getCategoryBooks()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getCategoryBooks()
}

// 跳转到书籍详情
const goToBookDetail = (bookId) => {
  router.push(`/book/${bookId}`)
}

// 跳转到首页
const goToHome = () => {
  router.push('/')
}

// 页面加载时获取分类书籍列表
onMounted(() => {
  getCategoryBooks()
})
</script>

<style scoped>
.category-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background-color: #409EFF;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  margin: 0;
  font-size: 20px;
}

.category-title {
  margin: 20px 0;
}

.category-title h2 {
  margin: 0;
  color: #303133;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.book-card {
  transition: all 0.3s ease;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.book-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.book-price {
  font-size: 18px;
  font-weight: bold;
  color: #F56C6C;
}

.book-card-body {
  display: flex;
  gap: 15px;
  margin: 15px 0;
}

.book-image {
  flex-shrink: 0;
}

.book-image img {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 4px;
}

.book-info {
  flex: 1;
}

.book-info p {
  margin: 5px 0;
  font-size: 14px;
  color: #606266;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.footer {
  background-color: #f5f7fa;
  text-align: center;
  line-height: 60px;
  margin-top: auto;
}
</style>