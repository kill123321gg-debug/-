<template>
  <div class="address-container">
    <el-header height="60px" class="header">
      <div class="header-content">
        <h1 class="logo">校园二手书交易平台</h1>
        <div class="header-right">
          <el-button type="primary" @click="goToHome">首页</el-button>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <div class="address-title">
        <h2>地址管理</h2>
        <el-button type="primary" @click="dialogVisible = true">新增地址</el-button>
      </div>
      
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else-if="addresses.length > 0" class="address-list">
        <el-card v-for="address in addresses" :key="address.id" class="address-card">
          <div class="address-content">
            <div class="address-header">
              <span class="receiver">{{ address.receiver }} {{ address.phone }}</span>
              <span v-if="address.is_default" class="default-tag">默认</span>
            </div>
            <div class="address-info">
              <p>{{ address.address }}</p>
            </div>
            <div class="address-actions">
              <el-button size="small" @click="editAddress(address)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteAddress(address.id)">删除</el-button>
              <el-button v-if="!address.is_default" size="small" type="primary" @click="setDefault(address.id)">设为默认</el-button>
            </div>
          </div>
        </el-card>
      </div>
      <div v-else class="no-addresses">
        <el-empty description="暂无地址" />
        <el-button type="primary" @click="dialogVisible = true">添加地址</el-button>
      </div>
      
      <!-- 新增/编辑地址对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
      >
        <el-form :model="addressForm" :rules="addressRules" ref="addressFormRef" label-width="80px">
          <el-form-item label="收货人" prop="receiver">
            <el-input v-model="addressForm.receiver" placeholder="请输入收货人姓名" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="addressForm.phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="地址" prop="address">
            <el-input v-model="addressForm.address" type="textarea" placeholder="请输入详细地址" :rows="3" />
          </el-form-item>
          <el-form-item>
            <el-checkbox v-model="addressForm.is_default">设为默认地址</el-checkbox>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleSave">保存</el-button>
          </span>
        </template>
      </el-dialog>
    </el-main>
    
    <el-footer height="60px" class="footer">
      <p>© 2026 校园二手书交易平台</p>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(true)
const addresses = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新增地址')
const addressFormRef = ref(null)
const editingAddressId = ref(null)

const addressForm = reactive({
  receiver: '',
  phone: '',
  address: '',
  is_default: false
})

const addressRules = {
  receiver: [
    { required: true, message: '请输入收货人姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入详细地址', trigger: 'blur' }
  ]
}

// 获取地址列表
const getAddresses = async () => {
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
    const response = await fetch(`/api/addresses?user_id=${userObj.id}`)
    const data = await response.json()
    if (data.code === 200) {
      addresses.value = data.addresses
    }
  } catch (error) {
    console.error('获取地址列表失败:', error)
    ElMessage.error('获取地址列表失败')
  } finally {
    loading.value = false
  }
}

// 新增地址
const addAddress = async () => {
  if (!addressFormRef.value) return
  
  await addressFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        const response = await fetch('/api/addresses', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            ...addressForm,
            user_id: user.id
          })
        })
        const data = await response.json()
        if (data.code === 200) {
          ElMessage.success('地址添加成功')
          dialogVisible.value = false
          getAddresses()
        } else {
          ElMessage.error(data.message)
        }
      } catch (error) {
        console.error('添加地址失败:', error)
        ElMessage.error('添加地址失败')
      }
    }
  })
}

// 编辑地址
const updateAddress = async () => {
  if (!addressFormRef.value) return
  
  await addressFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await fetch(`/api/addresses/${editingAddressId.value}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(addressForm)
        })
        const data = await response.json()
        if (data.code === 200) {
          ElMessage.success('地址更新成功')
          dialogVisible.value = false
          getAddresses()
        } else {
          ElMessage.error(data.message)
        }
      } catch (error) {
        console.error('更新地址失败:', error)
        ElMessage.error('更新地址失败')
      }
    }
  })
}

// 处理保存
const handleSave = () => {
  if (editingAddressId.value) {
    updateAddress()
  } else {
    addAddress()
  }
}

// 编辑地址
const editAddress = (address) => {
  editingAddressId.value = address.id
  dialogTitle.value = '编辑地址'
  addressForm.receiver = address.receiver
  addressForm.phone = address.phone
  addressForm.address = address.address
  addressForm.is_default = address.is_default
  dialogVisible.value = true
}

// 删除地址
const deleteAddress = async (addressId) => {
  try {
    const response = await fetch(`/api/addresses/${addressId}`, {
      method: 'DELETE'
    })
    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('地址删除成功')
      getAddresses()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    console.error('删除地址失败:', error)
    ElMessage.error('删除地址失败')
  }
}

// 设置默认地址
const setDefault = async (addressId) => {
  try {
    const response = await fetch(`/api/addresses/${addressId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_default: true })
    })
    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('设置默认地址成功')
      getAddresses()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    console.error('设置默认地址失败:', error)
    ElMessage.error('设置默认地址失败')
  }
}

// 跳转到首页
const goToHome = () => {
  router.push('/')
}

// 页面加载时获取地址列表
onMounted(() => {
  getAddresses()
})
</script>

<style scoped>
.address-container {
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

.address-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.address-title h2 {
  margin: 0;
  color: #303133;
}

.loading-container {
  margin: 20px 0;
}

.address-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.address-card {
  transition: all 0.3s ease;
}

.address-card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.address-content {
  padding: 15px;
}

.address-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.receiver {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.default-tag {
  background-color: #409EFF;
  color: white;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
}

.address-info {
  margin-bottom: 15px;
}

.address-info p {
  margin: 0;
  color: #606266;
  line-height: 1.5;
}

.address-actions {
  display: flex;
  gap: 10px;
}

.no-addresses {
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