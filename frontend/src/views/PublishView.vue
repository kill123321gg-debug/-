<template>
  <div class="publish-container">
    <el-header height="60px" class="header">
      <div class="header-content">
        <h1 class="logo">校园二手书交易平台</h1>
        <div class="header-right">
          <el-button type="primary" @click="goToHome">首页</el-button>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <el-card class="publish-card">
        <template #header>
          <div class="publish-header">
            <h2>发布二手书籍</h2>
          </div>
        </template>
        <el-form :model="publishForm" :rules="publishRules" ref="publishFormRef" label-width="100px">
          <el-form-item label="书名" prop="title">
            <el-input v-model="publishForm.title" placeholder="请输入书名" />
          </el-form-item>
          <el-form-item label="作者" prop="author">
            <el-input v-model="publishForm.author" placeholder="请输入作者" />
          </el-form-item>
          <el-form-item label="ISBN" prop="isbn">
            <el-input v-model="publishForm.isbn" placeholder="请输入ISBN" />
          </el-form-item>
          <el-form-item label="分类" prop="category">
            <el-select v-model="publishForm.category" placeholder="请选择分类">
              <el-option label="教材" value="教材" />
              <el-option label="教辅" value="教辅" />
              <el-option label="文学" value="文学" />
              <el-option label="科技" value="科技" />
              <el-option label="其他" value="其他" />
            </el-select>
          </el-form-item>
          <el-form-item label="成色" prop="condition">
            <el-select v-model="publishForm.condition" placeholder="请选择成色">
              <el-option label="全新" value="全新" />
              <el-option label="九成新" value="九成新" />
              <el-option label="八成新" value="八成新" />
              <el-option label="七成新" value="七成新" />
              <el-option label="六成新" value="六成新" />
              <el-option label="五成新" value="五成新" />
            </el-select>
          </el-form-item>
          <el-form-item label="价格" prop="price">
            <el-input v-model.number="publishForm.price" placeholder="请输入价格" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="publishForm.description" type="textarea" placeholder="请输入书籍描述" :rows="4" />
          </el-form-item>
          <el-form-item label="库存" prop="stock">
            <el-input v-model.number="publishForm.stock" placeholder="请输入库存，默认1" />
          </el-form-item>
          <el-form-item label="交易方式" prop="delivery_type">
            <el-select v-model="publishForm.delivery_type" placeholder="请选择交易方式">
              <el-option label="面交" value="面交" />
              <el-option label="快递" value="快递" />
              <el-option label="自取" value="自取" />
            </el-select>
          </el-form-item>
          <el-form-item label="图片" prop="images">
            <el-upload
              class="upload-demo"
              action="#"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :file-list="fileList"
              :auto-upload="false"
              :limit="3"
              :on-exceed="handleExceed"
            >
              <el-button type="primary">点击上传</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  最多上传3张图片
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handlePublish" :loading="loading">发布</el-button>
            <el-button @click="goToHome">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
    
    <el-footer height="60px" class="footer">
      <p>© 2026 校园二手书交易平台</p>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const publishFormRef = ref(null)
const loading = ref(false)
const fileList = ref([])

const publishForm = reactive({
  title: '',
  author: '',
  isbn: '',
  category: '',
  condition: '',
  price: '',
  description: '',
  stock: 1,
  delivery_type: '',
  images: []
})

const publishRules = {
  title: [
    { required: true, message: '请输入书名', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'blur' }
  ],
  condition: [
    { required: true, message: '请选择成色', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格必须大于0', trigger: 'blur' }
  ],
  delivery_type: [
    { required: true, message: '请选择交易方式', trigger: 'blur' }
  ]
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
  ElMessage.warning('最多只能上传3张图片')
}

// 处理发布
const handlePublish = async () => {
  if (!publishFormRef.value) return
  
  // 检查用户是否登录
  const user = localStorage.getItem('user')
  if (!user) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  await publishFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 模拟图片上传，实际项目中需要实现真实的图片上传功能
        const images = fileList.value.map(file => URL.createObjectURL(file.raw))
        
        const userObj = JSON.parse(user)
        const publishData = {
          ...publishForm,
          images,
          user_id: userObj.id
        }
        
        const response = await fetch('/api/books', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(publishData)
        })
        const data = await response.json()
        if (data.code === 200) {
          ElMessage.success('发布成功')
          // 跳转到首页
          router.push('/')
        } else {
          ElMessage.error(data.message)
        }
      } catch (error) {
        ElMessage.error('发布失败，请稍后重试')
        console.error('发布失败:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

// 跳转到首页
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.publish-container {
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

.publish-card {
  margin: 20px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.publish-header {
  text-align: center;
}

.publish-header h2 {
  margin: 0;
  color: #409EFF;
}

.el-form {
  margin-top: 20px;
}

.el-form-item {
  margin-bottom: 20px;
}

.footer {
  background-color: #f5f7fa;
  text-align: center;
  line-height: 60px;
  margin-top: auto;
}
</style>