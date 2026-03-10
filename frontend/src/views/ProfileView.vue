<template>
  <div class="profile-container">
    <el-header height="60px" class="header">
      <div class="header-content">
        <h1 class="logo">校园二手书交易平台</h1>
        <div class="header-right">
          <el-button type="primary" @click="goToHome">首页</el-button>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <div class="profile-title">
        <h2>个人中心</h2>
      </div>
      
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else-if="user" class="profile-content">
        <el-card class="profile-card">
          <template #header>
            <div class="profile-header">
              <div class="avatar-container">
                <el-avatar :size="100" :src="user.avatar || 'https://via.placeholder.com/100'">
                  {{ user.nickname.charAt(0) }}
                </el-avatar>
                <el-button type="primary" size="small" @click="dialogVisible = true">更换头像</el-button>
              </div>
              <div class="user-info">
                <h3>{{ user.nickname }}</h3>
                <p>用户名: {{ user.username }}</p>
                <p v-if="user.phone">手机号: {{ user.phone }}</p>
                <p v-if="user.email">邮箱: {{ user.email }}</p>
              </div>
            </div>
          </template>
          <div class="profile-actions">
            <el-button type="primary" @click="editProfileVisible = true">编辑资料</el-button>
            <el-button @click="goToOrders">我的订单</el-button>
            <el-button @click="goToAddress">地址管理</el-button>
            <el-button type="danger" @click="logout">退出登录</el-button>
          </div>
        </el-card>
        
        <!-- 编辑资料对话框 -->
        <el-dialog
          v-model="editProfileVisible"
          title="编辑资料"
          width="500px"
        >
          <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="80px">
            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="editForm.nickname" placeholder="请输入昵称" />
            </el-form-item>
            <el-form-item label="头像" prop="avatar">
              <el-upload
                class="upload-demo"
                action="#"
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                :file-list="avatarFileList"
                :auto-upload="false"
                :limit="1"
                :on-exceed="handleExceed"
              >
                <el-button type="primary">点击上传</el-button>
                <template #tip>
                  <div class="el-upload__tip">
                    请上传头像图片
                  </div>
                </template>
              </el-upload>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="editProfileVisible = false">取消</el-button>
              <el-button type="primary" @click="handleUpdateProfile">保存</el-button>
            </span>
          </template>
        </el-dialog>
      </div>
      <div v-else class="error-container">
        <el-empty description="用户信息不存在" />
        <el-button type="primary" @click="goToLogin">去登录</el-button>
      </div>
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
const user = ref(null)
const editProfileVisible = ref(false)
const dialogVisible = ref(false)
const editFormRef = ref(null)
const avatarFileList = ref([])

const editForm = reactive({
  nickname: '',
  avatar: ''
})

const editRules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' }
  ]
}

// 获取用户信息
const getUserInfo = async () => {
  // 检查用户是否登录
  const userStr = localStorage.getItem('user')
  if (!userStr) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  loading.value = true
  try {
    const userObj = JSON.parse(userStr)
    const response = await fetch(`/api/user/profile?user_id=${userObj.id}`)
    const data = await response.json()
    if (data.code === 200) {
      user.value = data.user
      editForm.nickname = data.user.nickname
      editForm.avatar = data.user.avatar
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  } finally {
    loading.value = false
  }
}

// 处理图片预览
const handlePreview = (file) => {
  console.log(file)
}

// 处理图片移除
const handleRemove = (file, fileList) => {
  console.log(file, fileList)
}

// 处理图片超出限制
const handleExceed = (files, fileList) => {
  ElMessage.warning('只能上传一张头像')
}

// 更新用户信息
const handleUpdateProfile = async () => {
  if (!editFormRef.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 模拟头像上传，实际项目中需要实现真实的图片上传功能
        let avatar = editForm.avatar
        if (avatarFileList.value.length > 0) {
          avatar = URL.createObjectURL(avatarFileList.value[0].raw)
        }
        
        const userObj = JSON.parse(localStorage.getItem('user'))
        const response = await fetch('/api/user/profile', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: userObj.id,
            nickname: editForm.nickname,
            avatar
          })
        })
        const data = await response.json()
        if (data.code === 200) {
          ElMessage.success('资料更新成功')
          editProfileVisible.value = false
          // 更新本地存储的用户信息
          localStorage.setItem('user', JSON.stringify(data.user))
          getUserInfo()
        } else {
          ElMessage.error(data.message)
        }
      } catch (error) {
        console.error('更新资料失败:', error)
        ElMessage.error('更新资料失败')
      }
    }
  })
}

// 退出登录
const logout = () => {
  localStorage.removeItem('user')
  ElMessage.success('退出登录成功')
  router.push('/login')
}

// 跳转到首页
const goToHome = () => {
  router.push('/')
}

// 跳转到登录页面
const goToLogin = () => {
  router.push('/login')
}

// 跳转到订单页面
const goToOrders = () => {
  router.push('/orders')
}

// 跳转到地址管理页面
const goToAddress = () => {
  router.push('/address')
}

// 页面加载时获取用户信息
onMounted(() => {
  getUserInfo()
})
</script>

<style scoped>
.profile-container {
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

.profile-title {
  margin: 20px 0;
}

.profile-title h2 {
  margin: 0;
  color: #303133;
}

.loading-container {
  margin: 20px 0;
}

.profile-content {
  margin: 20px 0;
}

.profile-card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  gap: 30px;
  align-items: center;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.user-info h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.user-info p {
  margin: 5px 0;
  color: #606266;
}

.profile-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
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