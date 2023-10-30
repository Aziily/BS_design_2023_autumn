<template>
  <div class="device-edit-container">
    <el-card>
      <div slot="header" class="card-head">
        <span>Edit Device</span>
      </div>
      <el-form ref="ruleForm" :model="FormData" :rules="ruleForm" class="demo-ruleForm">
        <el-form-item label="Device Name" prop="name">
          <el-input v-model="FormData.name" placeholder="Please input device name" />
        </el-form-item>
        <el-form-item label="Device Description" prop="description">
          <el-input v-model="FormData.description" placeholder="Please input device description" maxlength="100" />
        </el-form-item>
        <el-form-item label="Device IP" prop="ip">
          <el-input v-model="FormData.ip" placeholder="Please input device IP" maxlength="15" minlength="7" />
        </el-form-item>
        <el-form-item label="Device Status" prop="status">
          <el-radio-group v-model="FormData.status">
            <el-radio label="0">Offline</el-radio>
            <el-radio label="1">Online</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="editDevice">Edit</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { update } from '@/api/device'
import { getToken } from '@/utils/auth'

export default {
  name: 'EditDevice',
  data() {
    var checkIP = (rule, value, callback) => {
      if (!/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(value)) {
        callback(new Error('IP should be number'))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        name: [
          { min: 1, max: 20, message: 'Length should be 3 to 20', trigger: 'blur' }
        ],
        description: [
          { min: 0, max: 100, message: 'Length should be 3 to 100', trigger: 'blur' }
        ],
        ip: [
          { validator: checkIP, trigger: 'blur' },
          { min: 7, max: 15, message: 'Length should be 7 to 15', trigger: 'blur' }
        ],
        status: [
        ]
      },
      OriginData: this.$route.params.device,
      FormData: {
        name: this.$route.params.device ? this.$route.params.device.name : '',
        description: this.$route.params.device ? this.$route.params.device.description : '',
        ip: this.$route.params.device ? this.$route.params.device.ip : '',
        status: this.$route.params.device ? (this.$route.params.device.status === 0 ? '0' : '1') : '0'
      },
      did: this.$route.params.device ? this.$route.params.device.did : null
    }
  },
  mounted() {
    if (!this.$route.params.device) {
      this.$router.go(-1)
    }
  },
  methods: {
    editDevice() {
      if (this.did === null) {
        this.$message.error('Invalid device')
        this.$router.go(-1)
        return false
      }
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          console.log(this.did)
          var data = {
            name: this.FormData.name === '' ? null : this.FormData.name,
            description: this.FormData.description === '' ? null : this.FormData.description,
            ip: this.FormData.ip,
            status: this.FormData.status === '0' ? 0 : 1
          }
          update(getToken(), data, this.did).then(response => {
            this.$message({
              message: 'Edit device successfully',
              type: 'success'
            })
            this.$store.dispatch('device/list')
            this.$router.go(-1)
          }).catch(error => {
            console.log(error)
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
