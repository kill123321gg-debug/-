<template>
  <div class="search-container">
    <el-header height="60px" class="header">
      <div class="header-content">
        <h1 class="logo">校园二手书交易平台</h1>
        <div class="header-right">
          <el-button type="primary" @click="goToHome">首页</el-button>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <div class="search-filter">
        <el-form :model="searchForm" inline>
          <el-form-item label="分类">
            <el-select v-model="searchForm.category" placeholder="全部">
              <el-option label="全部" value="" />
              <el-option label="教材" value="教材" />
              <el-option label="教辅" value="教辅" />
              <el-option label="文学" value="文学" />
              <el-option label="科技" value="科技" />
              <el-option label="其他" value="其他" />
            </el-select>
          </el-form-item>
          <el-form-item label="价格区间">
            <el-input-number v-model="searchForm.min_price" placeholder="最低价" :min="0" />
            <span class="price-range">-</span>
            <el-input-number v-model="searchForm.max_price" placeholder="最高价" :min="0" />
          </el-form-item>
          <el-form-item label="成色">
            <el-select v-model="searchForm.condition" placeholder="全部">
              <el-option label="全部" value="" />
              <el-option label="全新" value="全新" />
              <el-option label="九成新" value="九成新" />
              <el-option label="八成新" value="八成新" />
              <el-option label="七成新" value="七成新" />
              <el-option label="六成新" value="六成新" />
              <el-option label="五成新" value="五成新" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">筛选</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="search-result">
        <h3>搜索结果: {{ searchKeyword }}</h3>
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="10" animated />
        </div>
        <div v-else-if="books.length > 0" class="book-list">
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
        <div v-else class="no-result">
          <el-empty description="没有找到相关书籍" />
        </div>
      </div>
    </el-main>
    
    <el-footer height="60px" class="footer">
      <p>© 2026 校园二手书交易平台</p>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const searchKeyword = ref(route.query.keyword || '')
const loading = ref(true)
const books = ref([])

const searchForm = ref({
  category: '',
  min_price: null,
  max_price: null,
  condition: ''
})

// 搜索书籍
const searchBooks = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (searchKeyword.value) {
      params.append('keyword', searchKeyword.value)
    }
    if (searchForm.value.category) {
      params.append('category', searchForm.value.category)
    }
    if (searchForm.value.min_price) {
      params.append('min_price', searchForm.value.min_price)
    }
    if (searchForm.value.max_price) {
      params.append('max_price', searchForm.value.max_price)
    }
    if (searchForm.value.condition) {
      params.append('condition', searchForm.value.condition)
    }
    
    const response = await fetch(`/api/books/search?${params.toString()}`)
    const data = await response.json()
    if (data.code === 200) {
      books.value = data.books
    }
  } catch (error) {
    console.error('搜索书籍失败:', error)
  } finally {
    loading.value = false
  }
}

// 处理搜索
const handleSearch = () => {
  searchBooks()
}

// 跳转到书籍详情
const goToBookDetail = (bookId) => {
  router.push(`/book/${bookId}`)
}

// 跳转到首页
const goToHome = () => {
  router.push('/')
}

// 页面加载时搜索书籍
onMounted(() => {
  searchBooks()
})
</script>

<style scoped>
.search-container {
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

.search-filter {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.price-range {
  margin: 0 10px;
}

.search-result {
  margin-top: 20px;
}

.search-result h3 {
  margin-bottom: 20px;
  color: #303133;
}

.loading-container {
  margin: 20px 0;
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

.no-result {
  margin: 40px 0;
}

.footer {
  background-color: #f5f7fa;
  text-align: center;
  line-height: 60px;
  margin-top: auto;
}
</style>