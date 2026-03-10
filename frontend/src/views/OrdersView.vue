<template>
  <div class="orders-container">
    <el-header height="60px" class="header">
      <div class="header-content">
        <h1 class="logo">校园二手书交易平台</h1>
        <div class="header-right">
          <el-button type="primary" @click="goToHome">首页</el-button>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <div class="orders-title">
        <h2>我的订单</h2>
      </div>
      
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else-if="orders.length > 0" class="orders-list">
        <el-card v-for="order in orders" :key="order.id" class="order-card">
          <template #header>
            <div class="order-header">
              <span class="order-no">订单号: {{ order.order_no }}</span>
              <span :class="['order-status', order.status]">{{ getStatusText(order.status) }}</span>
            </div>
          </template>
          <div class="order-content">
            <div class="order-book">
              <img :src="order.book.images[0] || 'https://via.placeholder.com/100'" alt="书籍封面" class="book-image" />
              <div class="book-info">
                <h3>{{ order.book.title }}</h3>
                <p>价格: ¥{{ order.total_price }}</p>
              </div>
            </div>
            <div class="order-address">
              <h4>收货地址</h4>
              <p>{{ order.address.receiver }} {{ order.address.phone }}</p>
              <p>{{ order.address.address }}</p>
            </div>
            <div class="order-time">
              <p>下单时间: {{ order.created_at }}</p>
            </div>
          </div>
          <template #footer>
            <div class="order-actions">
              <el-button @click="goToOrderDetail(order.id)">查看详情</el-button>
              <el-button v-if="order.status === 'pending'" type="danger" @click="cancelOrder(order.id)">取消订单</el-button>
              <el-button v-if="order.status === 'shipped'" type="primary" @click="confirmReceipt(order.id)">确认收货</el-button>
            </div>
          </template>
        </el-card>
      </div>
      <div v-else class="no-orders">
        <el-empty description="暂无订单" />
        <el-button type="primary" @click="goToHome">去购物</el-button>
      </div>
    </el-main>
    
    <el-footer height="60px" class="footer">
      <p>© 2026 校园二手书交易平台</p>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(true)
const orders = ref([])

// 获取订单列表
const getOrders = async () => {
  // 检查用户是否登录
  const user = localStorage.getItem('user')
  if (!user) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  loading.value = true
  try {
    const userObj = JSON.parse(user)
    const response = await fetch(`/api/orders?user_id=${userObj.id}`)
    const data = await response.json()
    if (data.code === 200) {
      orders.value = data.orders
    }
  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

// 获取订单状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待付款',
    'paid': '待发货',
    'shipped': '待收货',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

// 取消订单
const cancelOrder = async (orderId) => {
  try {
    const response = await fetch(`/api/orders/${orderId}/cancel`, {
      method: 'PUT'
    })
    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('订单取消成功')
      getOrders()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    console.error('取消订单失败:', error)
    ElMessage.error('取消订单失败')
  }
}

// 确认收货
const confirmReceipt = async (orderId) => {
  try {
    const response = await fetch(`/api/orders/${orderId}/confirm`, {
      method: 'PUT'
    })
    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('收货确认成功')
      getOrders()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    console.error('确认收货失败:', error)
    ElMessage.error('确认收货失败')
  }
}

// 跳转到订单详情
const goToOrderDetail = (orderId) => {
  router.push(`/order/${orderId}`)
}

// 跳转到首页
const goToHome = () => {
  router.push('/')
}

// 页面加载时获取订单列表
onMounted(() => {
  getOrders()
})
</script>

<style scoped>
.orders-container {
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

.orders-title {
  margin: 20px 0;
}

.orders-title h2 {
  margin: 0;
  color: #303133;
}

.loading-container {
  margin: 20px 0;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  transition: all 0.3s ease;
}

.order-card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-no {
  font-size: 14px;
  color: #606266;
}

.order-status {
  font-size: 14px;
  font-weight: bold;
}

.order-status.pending {
  color: #E6A23C;
}

.order-status.paid {
  color: #409EFF;
}

.order-status.shipped {
  color: #67C23A;
}

.order-status.completed {
  color: #909399;
}

.order-status.cancelled {
  color: #F56C6C;
}

.order-content {
  margin: 15px 0;
}

.order-book {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.book-image {
  width: 80px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

.book-info h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.book-info p {
  margin: 0;
  color: #F56C6C;
  font-weight: bold;
}

.order-address {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.order-address h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.order-address p {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}

.order-time {
  font-size: 14px;
  color: #909399;
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.no-orders {
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