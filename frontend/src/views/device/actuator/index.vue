<template>
  <!-- one card for each device -->
  <div class="device-actuator-container">
    <el-row>
      <el-col v-for="device in actuatorDevices" :key="device.id" :xs="24" :sm="12" :md="8" :lg="6" :xl="6">
        <el-card shadow="hover" class="device-card">
          <span class="device-id">{{ device.did }}</span>
          <span class="device-name">{{ device.name }}</span>
          <el-button class="device-full" style="float: right; padding: 3px 0" type="text" icon="el-icon-full-screen" size="mini" @click="openActuatorDetailDialog(device.did)" />
          <div class="device-description">
            <el-collapse>
              <el-collapse-item title="Description" name="1">
                <div style="word-wrap: break-word;white-space: pre-wrap;">
                  {{ device.description }}
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
          <li class="device-ip">IP: {{ device.ip }}</li>
          <li v-if="device.status === 0" class="device-status-off">Offline</li>
          <li v-else-if="device.status === 1" class="device-status-on">Online</li>
          <!-- a folded icon to hide the description -->
        </el-card>
      </el-col>
    </el-row>
    <!-- <el-row>{{ this.devices.filter(device => device.type === 0) }}</el-row>
    <el-row>{{ actuatorDevices }}</el-row> -->
    <div>
      <el-dialog
        id="actuator-detail-dialog"
        title="Actuator Detail"
        width="90%"
        :visible.sync="dialogVisible"
        :before-close="handleClose"
      >
        <el-row>
          <el-col :span="8" class="detail-head">
            <!-- id name and photo -->
            <div style="text-align: center" class="detail-name">
              <span>{{ curDevice.name }}</span>
            </div>
            <div style="text-align: center" class="detail-photo">
              <img src="https://tse1-mm.cn.bing.net/th/id/OIP-C.S1l6laEgs_yJJK99gAbQpAHaHa?pid=ImgDet&rs=1">
            </div>
          </el-col>
          <el-col :span="16">
            <!-- other -->
            <el-form :model="curDevice" class="detail-body">
              <el-form-item label="Device Description">
                <span>{{ curDevice.description }}</span>
              </el-form-item>
              <el-form-item label="Device IP">
                <span>{{ curDevice.ip }}</span>
              </el-form-item>
              <el-form-item label="Device Status">
                <span>{{ curDevice.status === 0 ? 'Offline' : 'Online' }}</span>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>
        <el-row>
          <div class="detail-data">
            <!-- <div v-for="data in dataDates" :key="data.id">
              <span>{{ data }}</span>
            </div> -->
            <div class="dropdown-div">
              <el-dropdown trigger="click" @command="chooseDate = $event">
                <span class="el-dropdown-link">
                  {{ chooseDate || 'Choose Date' }}
                  <i class="el-icon-arrow-down el-icon--right" />
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item v-for="date in dataDates.keys()" :key="date" :command="date">
                    {{ date }}
                  </el-dropdown-item>
                  <el-dropdown-item v-if="dataDates.size === 0" disabled>
                    No Data
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
            <div class="chart-div">
              <div class="detail-chart" style="width: 100%; height: 100%" />
            </div>
          </div>
        </el-row>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { info, data } from '@/api/device'
import { getToken } from '@/utils/auth'
import echarts from 'echarts'

export default {
  name: 'DeviceActuator',
  data() {
    return {
      actuatorDevices: [],
      curDevice: {},
      deviceData: [],
      dataDates: new Map(),
      chooseDate: '',
      dialogVisible: false
    }
  },
  computed: {
    ...mapGetters([
      'devices'
    ])
  },
  watch: {
    devices: {
      handler() {
        this.setData()
      },
      deep: true
    },
    chooseDate: {
      handler() {
        this.drawChart()
      },
      deep: true
    }
  },
  mounted() {
    this.setData()
  },
  methods: {
    setData() {
      this.actuatorDevices = this.devices.filter(device => device.type === 1)
    },
    openActuatorDetailDialog(did) {
      var token = getToken()
      info(token, did).then(response => {
        // console.log(response)
        this.curDevice = response.data
        data(token, did).then(response => {
          // console.log(response)
          this.deviceData = response.data
          this.setDates()
          this.dialogVisible = true
        }).catch(error => {
          // alert(error)
          console.log(error)
        })
      }).catch(error => {
        // alert(error)
        console.log(error)
      })
    },
    setDates() {
      this.dataDates = new Map()
      // sort
      this.deviceData = this.deviceData.sort((a, b) => {
        return a.timestamp - b.timestamp
      })
      for (var i = 0; i < this.deviceData.length; i++) {
        var date = new Date(this.deviceData[i].timestamp)
        var year = date.getFullYear()
        var month = date.getMonth() + 1
        var day = date.getDate()
        var key = year + '-' + month + '-' + day
        if (!this.dataDates.has(key)) {
          this.dataDates.set(key, [])
        }
        this.dataDates.get(key).push({
          data: this.deviceData[i].data
        })
      }
    },
    drawChart() {
      // true: on, false: off
      var data = this.dataDates.get(this.chooseDate)
      var on = 0
      var off = 0
      console.log(data)
      for (var i = 0; i < data.length; i++) {
        if (data[i].data === true) {
          on++
        } else {
          off++
        }
      }
      var chart = echarts.init(document.getElementsByClassName('detail-chart')[0])
      chart.clear()
      chart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        series: [
          {
            name: 'Actuator Data',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [
              { value: on, name: 'On' },
              { value: off, name: 'Off' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, .5)'
              }
            }
          }
        ]
      })
    },
    handleClose(done) {
      this.dialogVisible = false
      this.chooseDate = ''
      this.dataDates = new Map()
      this.curDevice = {}
      var chart = echarts.init(document.getElementsByClassName('detail-chart')[0])
      chart.clear()
      done()
    }
  }
}
</script>

<!-- card view -->
<style lang="scss" scoped>

.device-card {
  padding: 10px;
  margin: 10px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  cursor: pointer;
}
.device-actuator-container {
  margin: 20px;
}
.device-id {
  font-size: 16px;
  font-weight: bold;
}
.device-name {
  font-size: 16px;
  font-weight: bold;
  margin-left: 10px;
}
.device-full {
  margin-right: 8px;
}
.device-description {
  // grey font
  font-size: 8px;
  font-style: italic;
  margin: 10px 0px;
}

.device-ip {
  font-size: 14px;
  margin: 10px 0;
}
.device-status-off {
  font-size: 14px;
  margin: 10px 0;
  color: #f56c6c; // light red
}
.device-status-on {
  font-size: 14px;
  margin: 10px 0;
  color: #67c23a; // light green
}

</style>

<!-- dialog view -->
<style lang="scss" scoped>
.detail-head {
  margin: 16px 0px;
  .detail-name {
    font-family: 'Roboto', sans-serif;
    font-size: 24px;
    margin: 12px 0px;
    padding-right: 12px;
  }
  .detail-photo {
    margin: 12px 0px;
    padding-right: 12px;
  }
  img {
    width: 100px;
    height: 100px;
  }
}
.detail-body {
  margin: 16px 0;
}
.detail-data {
  margin: 16px 0;

  .dropdown-div {
    text-align: center;
  }
  .chart-div {
    margin: 10px 0;
    width: 100%;
    height: 278px;
  }
}
</style>
