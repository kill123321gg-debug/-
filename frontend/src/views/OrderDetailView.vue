<template>
  <div class="order-detail-container">
    <el-header height="60px" class="header">
      <div class="header-content">
        <h1 class="logo">校园二手书交易平台</h1>
        <div class="header-right">
          <el-button type="primary" @click="goToOrders">返回订单列表</el-button>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else-if="order" class="order-detail">
        <el-card class="order-card">
          <template #header>
            <div class="order-header">
              <h2>订单详情</h2>
              <span :class="['order-status', order.status]">{{ getStatusText(order.status) }}</span>
            </div>
          </template>
          <div class="order-info">
            <div class="order-basic">
              <p><strong>订单号:</strong> {{ order.order_no }}</p>
              <p><strong>下单时间:</strong> {{ order.created_at }}</p>
              <p><strong>更新时间:</strong> {{ order.updated_at }}</p>
            </div>
            
            <div class="order-book">
              <h3>商品信息</h3>
              <div class="book-item">
                <img :src="order.book.images[0] || 'https://via.placeholder.com/100'" alt="书籍封面" class="book-image" />
                <div class="book-info">
                  <h4>{{ order.book.title }}</h4>
                  <p>作者: {{ order.book.author }}</p>
                  <p>价格: ¥{{ order.total_price }}</p>
                </div>
              </div>
            </div>
            
            <div class="order-address">
              <h3>收货地址</h3>
              <div class="address-info">
                <p><strong>收货人:</strong> {{ order.address.receiver }}</p>
                <p><strong>手机号:</strong> {{ order.address.phone }}</p>
                <p><strong>地址:</strong> {{ order.address.address }}</p>
              </div>
            </div>
            
            <div class="order-total">
              <p><strong>总价:</strong> ¥{{ order.total_price }}</p>
            </div>
          </div>
          <template #footer>
            <div class="order-actions">
              <el-button @click="goToOrders">返回订单列表</el-button>
              <el-button v-if="order.status === 'pending'" type="danger" @click="cancelOrder(order.id)">取消订单</el-button>
              <el-button v-if="order.status === 'shipped'" type="primary" @click="confirmReceipt(order.id)">确认收货</el-button>
            </div>
          </template>
        </el-card>
      </div>
      <div v-else class="error-container">
        <el-empty description="订单不存在" />
        <el-button type="primary" @click="goToOrders">返回订单列表</el-button>
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
const orderId = ref(route.params.id)
const loading = ref(true)
const order = ref(null)

// 获取订单详情
const getOrderDetail = async () => {
  try {
    const response = await fetch(`/api/orders/${orderId.value}`)
    const data = await response.json()
    if (data.code === 200) {
      order.value = data.order
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    console.error('获取订单详情失败:', error)
    ElMessage.error('获取订单详情失败')
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
      getOrderDetail()
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
      getOrderDetail()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    console.error('确认收货失败:', error)
    ElMessage.error('确认收货失败')
  }
}

// 跳转到订单列表
const goToOrders = () => {
  router.push('/orders')
}

// 页面加载时获取订单详情
onMounted(() => {
  getOrderDetail()
})
</script>

<style scoped>
.order-detail-container {
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

.order-detail {
  margin: 20px 0;
}

.order-card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-header h2 {
  margin: 0;
  color: #303133;
}

.order-status {
  font-size: 16px;
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

.order-info {
  margin: 20px 0;
}

.order-basic {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.order-basic p {
  margin: 5px 0;
  color: #606266;
}

.order-book {
  margin-bottom: 20px;
}

.order-book h3 {
  margin: 0 0 15px 0;
  color: #303133;
}

.book-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.book-image {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 4px;
}

.book-info h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.book-info p {
  margin: 5px 0;
  color: #606266;
}

.order-address {
  margin-bottom: 20px;
}

.order-address h3 {
  margin: 0 0 15px 0;
  color: #303133;
}

.address-info {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.address-info p {
  margin: 5px 0;
  color: #606266;
}

.order-total {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  text-align: right;
}

.order-total p {
  margin: 0;
  font-size: 16px;
  color: #F56C6C;
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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