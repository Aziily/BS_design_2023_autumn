<template>
  <div class="device-add-container">
    <el-card>
      <div slot="header" class="card-head">
        <span>Add Device</span>
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
        <el-form-item label="Device Kind" prop="type">
          <!-- single selection -->
          <el-select v-model="FormData.type" placeholder="Please select device kind">
            <el-option label="Sensor" value="sensor" />
            <el-option label="Actuator" value="actuator" />
          </el-select>
        </el-form-item>
        <el-form-item label="Device Status" prop="status">
          <el-radio-group v-model="FormData.status">
            <el-radio label="0">Offline</el-radio>
            <el-radio label="1">Online</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addDevice">Add</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { add } from '@/api/device'
import { getToken } from '@/utils/auth'

export default {
  name: 'AddDevice',
  data() {
    var checkIP = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input device IP'))
      } else if (!/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(value)) {
        callback(new Error('IP should be number'))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        name: [
          { required: true, message: 'Please input device name', trigger: 'blur' },
          { min: 1, max: 20, message: 'Length should be 3 to 20', trigger: 'blur' }
        ],
        description: [
          { min: 0, max: 100, message: 'Length should be 3 to 100', trigger: 'blur' }
        ],
        ip: [
          { required: true, message: 'Please input device IP', trigger: 'blur' },
          { validator: checkIP, trigger: 'blur' },
          { min: 7, max: 15, message: 'Length should be 7 to 15', trigger: 'blur' }
        ],
        type: [
          { required: true, message: 'Please select device kind', trigger: 'blur' }
        ],
        status: [
          { required: true, message: 'Please select device status', trigger: 'blur' }
        ]
      },
      FormData: {
        name: '',
        description: '',
        ip: '',
        type: this.$route.params.type ? this.$route.params.type : 'sensor',
        status: '0'
      }
    }
  },
  mounted() {
    console.log(this.FormData.type)
  },
  methods: {
    addDevice() {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          // console.log(this.FormData)
          var data = {
            name: this.FormData.name,
            description: this.FormData.description === '' ? null : this.FormData.description,
            type: this.FormData.type === 'sensor' ? 0 : 1,
            ip: this.FormData.ip,
            status: this.FormData.status === '0' ? 0 : 1
          }
          add(getToken(), data).then(response => {
            this.$message({
              message: 'Add device successfully',
              type: 'success'
            })
            this.$store.dispatch('device/list')
            this.$router.push({ path: '/device/' + this.FormData.type })
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
