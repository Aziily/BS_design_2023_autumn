<template>
  <div class="user-update-container">
    <el-card>
      <div slot="header" class="card-head">
        <span>Update User</span>
      </div>
      <el-form ref="ruleForm" :model="FormData" :rules="ruleForm" class="demo-ruleForm">
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
          <el-button type="primary" @click="updateUser">Edit</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { update } from '@/api/user'
import { getToken } from '@/utils/auth'

export default {
  name: 'UserEdit',
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
        password: '',
        email: '',
        phone: ''
      },
      uid: -1
    }
  },
  mounted() {
    if (Object.prototype.hasOwnProperty.call(this.$route.params, 'user') === false) {
      this.$router.go(-1)
    }
    this.FormData.email = this.$route.params.user.email
    this.FormData.phone = this.$route.params.user.phone
    this.uid = this.$route.params.user.uid
    if (this.uid === -1) {
      this.$router.go(-1)
    }
  },
  methods: {
    updateUser() {
      // console.log(this.FormData)
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          // console.log(this.FormData)
          var data = {
            password: this.FormData.password,
            email: this.FormData.email,
            phone: this.FormData.phone
          }
          update(getToken(), data, this.uid).then(response => {
            this.$message({
              message: 'Update device successfully',
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
.user-update-container {
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
