<template>
  <div class="message-container">

    <div class="search-form"> <!-- type, time(year, month, day), level -->
      <el-card>
        <div slot="header" class="card-head">
          <span>Message</span>
        </div>
        <el-form ref="query" :model="query" label-width="100px" class="demo-ruleForm">
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
      <el-table :data="messageList.slice(curPage * 20, (curPage + 1) * 20)" border style="width: 100%">
        <el-table-column prop="did" label="Device ID" width="85" />
        <el-table-column prop="type" label="Type" width="80" />
        <el-table-column prop="time" label="Time" width="160" />
        <el-table-column prop="level" label="Level" width="90">
          <template slot-scope="scope">
            <el-tag :type="scope.row.level === 'error' ? 'danger' : scope.row.level">{{ scope.row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="Message">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>{{ scope.row.message }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium">{{ scope.row.message }}</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column prop="data" label="Data" width="100">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>{{ scope.row.data }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium">{{ scope.row.data }}</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          :current-page="curPage + 1"
          :page-size="20"
          layout="prev, pager, next"
          :total="messageList.length"
          @current-change="curPage = $event - 1"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { dataList, getDataYear } from '@/api/device'
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
      years: [],
      months: [],
      days: [],
      curPage: 0
    }
  },
  watch: {
    query: {
      handler: function(val, oldVal) {
        console.log(val)
        if (val.year === '-') {
          this.months = []
          this.days = []
          this.query.month = '-'
          this.query.day = '-'
        } else {
          this.months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
          if (val.month === '-') {
            this.days = []
            this.query.day = '-'
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
  mounted() {
    getDataYear().then(response => {
      this.years = response.data
    }).catch(error => {
      console.log(error)
    })
  },
  methods: {
    mapSensor(sensorMessage) {
      var timestamp = sensorMessage.timestamp
      if (timestamp.toString().length === 10) {
        timestamp = timestamp * 1000
      }
      var date = new Date(timestamp)
      var year = date.getFullYear()
      var month = date.getMonth() + 1
      var day = date.getDate()
      var hour = date.getHours()
      var minute = date.getMinutes()
      var second = date.getSeconds()
      var time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
      var level = sensorMessage.level === 0 ? 'info' : (sensorMessage.level === 1 ? 'warning' : 'error')
      return {
        id: 'sensor-' + sensorMessage.sdid.toString() + '-' + timestamp.toString(),
        did: sensorMessage.did.toString(),
        type: 'sensor',
        timestamp: timestamp,
        time: time,
        level: level,
        message: sensorMessage.message,
        data: sensorMessage.data
      }
    },
    mapActuator(actuatorMessage) {
      var timestamp = actuatorMessage.timestamp
      if (timestamp.toString().length === 10) {
        timestamp = timestamp * 1000
      }
      var date = new Date(timestamp)
      var year = date.getFullYear()
      var month = date.getMonth() + 1
      var day = date.getDate()
      var hour = date.getHours()
      var minute = date.getMinutes()
      var second = date.getSeconds()
      var time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
      var level = actuatorMessage.level === 0 ? 'info' : (actuatorMessage.level === 1 ? 'warning' : 'error')
      return {
        id: 'actuator-' + actuatorMessage.adid.toString() + '-' + timestamp.toString(),
        did: actuatorMessage.did.toString(),
        type: 'actuator',
        timestamp: timestamp,
        time: time,
        level: level,
        message: actuatorMessage.message,
        data: actuatorMessage.data ? 'on' : 'off'
      }
    },
    queryMessage() {
      // console.log(this.query)
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
        console.log(response.data.actuator)
        this.sensorMessages = response.data.sensor ? response.data.sensor.map(this.mapSensor) : []
        this.actuatorMessages = response.data.actuator ? response.data.actuator.map(this.mapActuator) : []
        this.messageList = this.sensorMessages.concat(this.actuatorMessages).sort((a, b) => {
          return a.timestamp - b.timestamp
        })
        this.curPage = 0
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.message-container {
  .message-list {
    margin: 32px;
    .pagination {
      margin-top: 16px;
      display: flex;
      justify-content: center;
    }
  }
}
</style>
