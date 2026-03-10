<template>
  <div class="book-detail-container">
    <el-header height="60px" class="header">
      <div class="header-content">
        <h1 class="logo">校园二手书交易平台</h1>
        <div class="header-right">
          <el-button type="primary" @click="goToHome">首页</el-button>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else-if="book" class="book-detail">
        <div class="book-info">
          <div class="book-images">
            <el-carousel :interval="4000" type="card" height="400px">
              <el-carousel-item v-for="(image, index) in book.images" :key="index">
                <img :src="image" alt="书籍图片" class="book-image" />
              </el-carousel-item>
            </el-carousel>
          </div>
          <div class="book-details">
            <h2>{{ book.title }}</h2>
            <p class="author">作者: {{ book.author }}</p>
            <p class="isbn">ISBN: {{ book.isbn }}</p>
            <p class="category">分类: {{ book.category }}</p>
            <p class="condition">成色: {{ book.condition }}</p>
            <p class="delivery-type">交易方式: {{ book.delivery_type }}</p>
            <p class="price">价格: ¥{{ book.price }}</p>
            <p class="stock" v-if="book.stock > 0">库存: {{ book.stock }}本</p>
            <p class="stock out-of-stock" v-else>库存: 已售罄</p>
            <div class="book-actions">
              <el-button type="primary" size="large" @click="buyNow" :disabled="book.stock <= 0">立即购买</el-button>
              <el-button size="large">收藏</el-button>
            </div>
          </div>
        </div>
        <div class="book-description">
          <h3>书籍描述</h3>
          <p>{{ book.description || '暂无描述' }}</p>
        </div>
      </div>
      <div v-else class="error-container">
        <el-empty description="书籍不存在" />
        <el-button type="primary" @click="goToHome">返回首页</el-button>
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
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const bookId = ref(route.params.id)
const book = ref(null)
const loading = ref(true)

// 获取书籍详情
const getBookDetail = async () => {
  try {
    const response = await fetch(`/api/books/${bookId.value}`)
    const data = await response.json()
    if (data.code === 200) {
      book.value = data.book
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    console.error('获取书籍详情失败:', error)
    ElMessage.error('获取书籍详情失败')
  } finally {
    loading.value = false
  }
}

// 立即购买
const buyNow = () => {
  // 检查用户是否登录
  const user = localStorage.getItem('user')
  if (!user) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  // 跳转到地址选择页面，然后创建订单
  router.push(`/order/create?book_id=${bookId.value}`)
}

// 跳转到首页
const goToHome = () => {
  router.push('/')
}

// 页面加载时获取书籍详情
onMounted(() => {
  getBookDetail()
})
</script>

<style scoped>
.book-detail-container {
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

.loading-container {
  margin: 20px 0;
}

.book-detail {
  margin: 20px 0;
}

.book-info {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-images {
  flex: 1;
  max-width: 400px;
}

.book-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.book-details {
  flex: 1;
}

.book-details h2 {
  margin-top: 0;
  color: #303133;
}

.author, .isbn, .category, .condition, .delivery-type {
  margin: 10px 0;
  color: #606266;
}

.price {
  margin: 20px 0;
  font-size: 24px;
  font-weight: bold;
  color: #F56C6C;
}

.stock {
  margin: 10px 0;
  color: #67C23A;
}

.out-of-stock {
  color: #F56C6C;
}

.book-actions {
  margin-top: 30px;
  display: flex;
  gap: 20px;
}

.book-description {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-description h3 {
  margin-top: 0;
  color: #303133;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 20px;
}

.footer {
  background-color: #f5f7fa;
  text-align: center;
  line-height: 60px;
  margin-top: auto;
}
</style>