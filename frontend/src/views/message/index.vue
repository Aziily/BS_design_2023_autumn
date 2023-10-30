<template>
  <div class="message-container">

    <div class="search-form"> <!-- type, time(year, month, day), level -->
      <el-card>
        <div slot="header" class="card-head">
          <span>Message</span>
        </div>
        <el-form ref="query" :model="query" :rules="queryRules" label-width="100px" class="demo-ruleForm">
          <div>
            <el-form-item label="Type" prop="type" width="40vw">
              <el-select v-model="query.type" placeholder="Please select message type">
                <el-option label="All" value="-" />
                <el-option label="Sensor" value="sensor" />
                <el-option label="Actuator" value="actuator" />
              </el-select>
            </el-form-item>
            <el-form-item label="Level" prop="level">
              <el-select v-model="query.level" placeholder="Please select message level">
                <el-option label="All" value="-" />
                <el-option label="Info" value="info" />
                <el-option label="Warning" value="warning" />
                <el-option label="Error" value="error" />
              </el-select>
            </el-form-item>
          </div>
          <el-form-item label="Date" prop="date">
            <el-select v-model="query.year" placeholder="Please select year">
              <el-option label="All" value="-" />
              <el-option v-for="year in years" :key="year" :label="year" :value="year" />
            </el-select>
            <el-select v-model="query.month" placeholder="Please select month">
              <el-option label="All" value="-" />
              <el-option v-for="month in months" :key="month" :label="month" :value="month" />
            </el-select>
            <el-select v-model="query.day" placeholder="Please select day">
              <el-option label="All" value="-" />
              <el-option v-for="day in days" :key="day" :label="day" :value="day" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="queryMessage">Query</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <div class="message-list">
      <span v-for="message in messageList" :key="message.id">message</span>
    </div>
  </div>
</template>

<script>
import { dataList } from '@/api/device'
import { getToken } from '@/utils/auth'

export default {
  name: 'Message',
  data() {
    return {
      query: {
        type: '-',
        year: '-',
        month: '-',
        day: '-',
        level: '-'
      },
      sensorMessages: [],
      actuatorMessages: [],
      messageList: [],
      years: [2020, 2021, 2022, 2023],
      months: [],
      days: []
    }
  },
  watch: {
    query: {
      handler: function(val, oldVal) {
        if (val.year === '-') {
          this.months = []
          this.days = []
        } else {
          if (val.month === '-') {
            this.days = []
          } else {
            var year = parseInt(val.year)
            var month = parseInt(val.month)
            var days = new Date(year, month, 0).getDate()
            this.days = []
            for (var i = 1; i <= days; i++) {
              this.days.push(i)
            }
          }
        }
      },
      deep: true
    }
  },
  methods: {
    queryMessage() {
      console.log(this.query)
      var data = {}
      if (this.query.type !== '-') {
        data.type = this.query.type === 'sensor' ? 0 : 1
      }
      if (this.query.year !== '-') {
        data.year = parseInt(this.query.year)
      }
      if (this.query.month !== '-') {
        data.month = parseInt(this.query.month)
      }
      if (this.query.day !== '-') {
        data.day = parseInt(this.query.day)
      }
      if (this.query.level !== '-') {
        data.level = this.query.level === 'info' ? 0 : (this.query.level === 'warning' ? 1 : 2)
      }
      dataList(getToken(), data).then(response => {
        console.log(response)
        var { sensors, actuators } = response.data
        this.sensorMessages = sensors
        this.actuatorMessages = actuators
        this.messageList = sensors.concat(actuators).sort((a, b) => {
          return b.timestamp - a.timestamp
        })
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>
