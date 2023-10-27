<template>
  <el-col style="margin-left:8px;" class="device-summary">
    <el-card class="device-summary">
      <el-col>
        <el-row>
          <span class="device-summary-head">Device Summary</span>
        </el-row>
        <!-- <el-row>{{ devices }}</el-row> -->
        <el-row>
          <el-col :span="12">
            <div class="online-device">
              <el-row><span class="head">Online</span></el-row>
              <el-row><span class="body">{{ onlineDevices }}</span></el-row>
            </div>
          </el-col>
          <el-col :span="6">
            <span class="split-line">/</span>
          </el-col>
          <el-col :span="12">
            <div class="total-device">
              <el-row><span class="head">Total</span></el-row>
              <el-row><span class="body">{{ totalDevices }}</span></el-row>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="package-count">
              <el-row><span class="head">Package</span></el-row>
              <el-row><span class="body">{{ packageCount }}</span></el-row>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-card>

    <el-card class="device-kind">
      <el-col>
        <el-row>
          <span class="device-kind-head">Device Kind</span>
        </el-row>
        <el-row>
          <el-col :span="20">
            <div class="sensor-device">
              <el-row><div id="sensor-device" style="width:100%;height:278px;float:left;"></div></el-row>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="actuator-device">
              <el-row><div id="actuator-device" style="width:100%;height:278px;float:left;"></div></el-row>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-card>

  </el-col>
</template>

<script>
import { mapGetters } from 'vuex'
import echarts from 'echarts'

export default {
  data() {
    return {
      onlineDevices: 0,
      totalDevices: 0,
      packageCount: 0,
      sensors: 0,
      actuators: 0,
      onlineSensors: 0,
      onlineActuators: 0
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
        this.drawSensorDevice()
        this.drawActuatorDevice()
      },
      deep: true
    }
  },
  mounted() {
    this.setData()
    this.drawSensorDevice()
    this.drawActuatorDevice()
  },
  methods: {
    setData() {
      this.onlineDevices = this.devices.filter(device => device.status === 1).length
      this.totalDevices = this.devices.length
      this.packageCount = 14514
      this.sensors = this.devices.filter(device => device.type === 0).length
      this.actuators = this.devices.filter(device => device.type === 1).length
      this.onlineSensors = this.devices.filter(device => device.type === 0 && device.status === 1).length
      this.onlineActuators = this.devices.filter(device => device.type === 1 && device.status === 1).length
    },
    drawSensorDevice() {
      var myChart = echarts.init(document.getElementById('sensor-device'))
      var option = {
        title: {
          text: 'Sensor Device',
          left: 'center',
          top: 20,
          textStyle: {
            color: '#ccc'
          },
          x: 'center'
        },
        grid: { containLabel: true },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c}'
        },
        series: [
          {
            name: 'Sensor Device',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: [
              { value: this.onlineSensors, name: 'Online' },
              { value: this.sensors - this.onlineSensors, name: 'Offline' }
            ],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, .5)'
              }
            }
          }
        ]
      }
      myChart.setOption(option)
    },
    drawActuatorDevice() {
      var myChart = echarts.init(document.getElementById('actuator-device'))
      var option = {
        title: {
          text: 'Actuator Device',
          left: 'center',
          top: 20,
          textStyle: {
            color: '#ccc'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c}'
        },
        series: [
          {
            name: 'Sensor Device',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: [
              { value: this.onlineActuators, name: 'Online' },
              { value: this.actuators - this.onlineActuators, name: 'Offline' }
            ],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, .5)'
              }
            }
          }
        ]
      }
      myChart.setOption(option)
    }
  }
}
</script>
