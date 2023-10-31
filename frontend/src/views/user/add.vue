<template>
  <div class="user-add-container">
    <el-card>
      <div slot="header" class="card-head">
        <span>Add User</span>
      </div>
      <el-form ref="ruleForm" :model="FormData" :rules="ruleForm" class="demo-ruleForm">
        <el-form-item label="Username" prop="username">
          <el-input v-model="FormData.username" placeholder="Please input username" />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="FormData.password" placeholder="Please input password" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="FormData.email" placeholder="Please input email" />
        </el-form-item>
        <el-form-item label="Phone" prop="phone">
          <el-input v-model="FormData.phone" placeholder="Please input phone" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addUser">Add</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { add } from '@/api/user'
import { getToken } from '@/utils/auth'

export default {
  name: 'UserAdd',
  data() {
    var checkPhone = (rule, value, callback) => {
      if (value === '') {
        callback()
      } else if (!/^1[3456789]\d{9}$/.test(value)) {
        callback(new Error('Please input correct phone'))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        username: [
          { required: true, message: 'Please input username', trigger: 'blur' },
          { min: 6, max: 20, message: 'Length should be 6 to 20', trigger: 'blur' }
        ],
        password: [
          { required: true, message: 'Please input password', trigger: 'blur' },
          { min: 6, max: 20, message: 'Length should be 6 to 20', trigger: 'blur' }
        ],
        email: [
          { required: true, message: 'Please input email', trigger: 'blur' },
          { type: 'email', message: 'Please input correct email', trigger: 'blur' }
        ],
        phone: [
          { required: false, message: 'Please input phone', trigger: 'blur' },
          { validator: checkPhone, trigger: 'blur' }
        ]
      },
      FormData: {
        username: '',
        password: '',
        email: '',
        phone: ''
      }
    }
  },
  methods: {
    addUser() {
      // console.log(this.FormData)
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          // console.log(this.FormData)
          var data = {
            username: this.FormData.username,
            password: this.FormData.password,
            email: this.FormData.email,
            phone: this.FormData.phone
          }
          add(getToken(), data).then(response => {
            this.$message({
              message: 'Add device successfully',
              type: 'success'
            })
            this.$router.push({ path: '/user' })
          }).catch(error => {
            // console.log(error)
            this.$message.error(error)
          })
        } else {
          this.$message.error('Invalid input')
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.user-add-container {
  .card-head {
    font-size: 24px;
    font-weight: bold;
    color: #000000;
  }
  .card-head::after {
    content: '';
    display: block;
    width: 80px;
    height: 2px;
    background-color: #000000;
    margin-top: 5px;
    margin-bottom: 20px;
  }
}
</style>
