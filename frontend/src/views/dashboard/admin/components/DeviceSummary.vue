<template>
  <el-col class="device-all">
    <el-card class="device-summary">
      <el-row>
        <span class="card-head">Device Summary</span>
      </el-row>
      <!-- <el-row>{{ devices }}</el-row> -->
      <el-row>
        <el-col class="online-data" :span="16">
          <div class="message-item">
            <div class="online-device">
              <el-row><span class="head">Online</span></el-row>
              <el-row><span class="body">{{ onlineDevices }}</span></el-row>
            </div>
            <div class="split-line"><span>/</span></div>
            <div class="total-device">
              <el-row><span class="body">{{ totalDevices }}</span></el-row>
            </div>
          </div>
        </el-col>
        <el-col class="package-count" :span="8">
          <div class="message-item">
            <div>
              <el-row><span class="head">Package</span></el-row>
              <el-row><span class="body">{{ sensorPackageCount + actuatorPackageCount }}</span></el-row>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="device-kind">
      <el-row>
        <span class="card-head">Device Kind</span>
      </el-row>
      <el-row>
        <el-col :xs="24" :sm="12" :md="12" :lg="8" :xl="8">
          <div class="device-chart">
            <div id="sensor-device" style="width:100%;height:100%;" />
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="12" :lg="8" :xl="8">
          <div class="device-chart">
            <div id="actuator-device" style="width:100%;height:100%;" />
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :md="24" :lg="8" :xl="8">
          <div class="device-chart">
            <div id="package-count" style="width:100%;height:100%;" />
          </div>
        </el-col>
      </el-row>
    </el-card>

  </el-col>
</template>

<script>
import { mapGetters } from 'vuex'
import { data } from '@/api/device'
import { getToken } from '@/utils/auth'
import echarts from 'echarts'

export default {
  data() {
    return {
      onlineDevices: 0,
      totalDevices: 0,
      sensorPackageCount: 0,
      actuatorPackageCount: 0,
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
      this.sensorPackageCount = 0
      this.actuatorPackageCount = 0
      if (this.devices.length !== 0) {
        for (let i = 0; i < this.devices.length; i++) {
          data(
            getToken(), this.devices[i].did
          ).then(response => {
            if (this.devices[i].type === 0) {
              this.sensorPackageCount += response.data.length
            } else {
              this.actuatorPackageCount += response.data.length
            }
            this.drawPackageCount()
          }).catch(error => {
            console.log(error)
          })
        }
      }
      this.sensors = this.devices.filter(device => device.type === 0).length
      this.actuators = this.devices.filter(device => device.type === 1).length
      this.onlineSensors = this.devices.filter(device => device.type === 0 && device.status === 1).length
      this.onlineActuators = this.devices.filter(device => device.type === 1 && device.status === 1).length
    },
    drawSensorDevice() {
      var myChart = echarts.init(document.getElementById('sensor-device'))
      // three color from light to deep (blue)
      var pieColor = ['#E8F2FF', '#5C9EFF']
      var option = {
        title: [
          {
            text: 'Sensor Online',
            subtext: 'Total: ' + this.sensors,
            textAlign: 'center',
            x: '50%',
            textStyle: {
              color: '#000000',
              fontSize: 16
            },
            padding: [0, 0, 20, 0]
          }
        ],
        legend: {
          show: false
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        series: [
          {
            name: 'base',
            type: 'pie',
            radius: [
              '60%',
              '70%'
            ],
            labelLine: {
              show: false
            },
            emphasis: {
              disabled: true
            },
            itemStyle: {
              color: pieColor[0]
            },
            data: [{
              value: this.sensors
            }]
          },
          {
            name: 'sensor-online',
            type: 'pie',
            zlevel: 1,
            startAngle: 90,
            radius: [
              '60%',
              '70%'
            ],
            avoidLabelOverlap: false,
            labelLine: {
              show: false
            },
            emphasis: {
              disabled: true
            },
            data: [
              {
                value: this.onlineSensors,
                name: 'online',
                itemStyle: {
                  color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 1,
                    y2: 1,
                    colorStops: [
                      {
                        offset: 0,
                        color: pieColor[1]
                      },
                      {
                        offset: 0.95,
                        color: pieColor[0]
                      }
                    ],
                    global: false
                  }
                },
                label: {
                  formatter: '{d}%',
                  position: 'center',
                  color: '#172B4D',
                  fontSize: 20
                }
              },
              {
                name: 'offline',
                label: {
                  show: false
                },
                itemStyle: {
                  normal: {
                    color: pieColor[0]
                  },
                  emphasis: {
                    color: pieColor[0]
                  }
                },
                value: this.sensors - this.onlineSensors
              }
            ]
          }
        ]
      }
      myChart.clear()
      myChart.setOption(option)
    },
    drawActuatorDevice() {
      var myChart = echarts.init(document.getElementById('actuator-device'))
      var pieColor = ['#E8F2FF', '#5C9EFF']
      var option = {
        title: [
          {
            text: 'Actuator Online',
            subtext: 'Total: ' + this.actuators,
            textAlign: 'center',
            x: '50%',
            textStyle: {
              color: '#000000',
              fontSize: 16
            },
            padding: [0, 0, 20, 0]
          }
        ],
        legend: {
          show: false
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        series: [
          {
            name: 'base',
            type: 'pie',
            radius: [
              '60%',
              '70%'
            ],
            labelLine: {
              show: false
            },
            emphasis: {
              disabled: true
            },
            itemStyle: {
              color: pieColor[0]
            },
            data: [{
              value: this.actuators
            }]
          },
          {
            name: 'actuator-online',
            type: 'pie',
            zlevel: 1,
            startAngle: 90,
            radius: [
              '60%',
              '70%'
            ],
            avoidLabelOverlap: false,
            labelLine: {
              show: false
            },
            emphasis: {
              disabled: true
            },
            data: [
              {
                value: this.onlineActuators,
                name: 'online',
                itemStyle: {
                  color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 1,
                    y2: 1,
                    colorStops: [
                      {
                        offset: 0,
                        color: pieColor[1]
                      },
                      {
                        offset: 0.95,
                        color: pieColor[0]
                      }
                    ],
                    global: false
                  }
                },
                label: {
                  formatter: '{d}%',
                  position: 'center',
                  color: '#172B4D',
                  fontSize: 20
                }
              },
              {
                name: 'offline',
                label: {
                  show: false
                },
                itemStyle: {
                  normal: {
                    color: pieColor[0]
                  },
                  emphasis: {
                    color: pieColor[0]
                  }
                },
                value: this.actuators - this.onlineActuators
              }
            ]
          }
        ]
      }
      myChart.clear()
      myChart.setOption(option)
    },
    drawPackageCount() {
      var myChart = echarts.init(document.getElementById('package-count'))
      var option = {
        title: {
          text: 'Package Count',
          subtext: 'Total: ' + (this.sensorPackageCount + this.actuatorPackageCount),
          textAlign: 'center',
          x: '50%',
          textStyle: {
            color: '#000000',
            fontSize: 16
          },
          padding: [0, 0, 20, 0]
        },
        xAxis: {
          type: 'category',
          data: ['Sensor', 'Actuator']
        },
        yAxis: {
          type: 'value',
          max: ((this.sensorPackageCount > this.actuatorPackageCount ? this.sensorPackageCount : this.actuatorPackageCount) * 1.1).toFixed(0)
        },
        series: [{
          data: [this.sensorPackageCount, this.actuatorPackageCount],
          type: 'bar',
          itemStyle: {
            // gradient color
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                {
                  offset: 0,
                  color: '#5C9EFF'
                },
                {
                  offset: 1,
                  color: '#E8F2FF'
                }
              ],
              global: false
            }
          }
        }]
      }
      myChart.setOption(option)
    }
  }
}
</script>

<style lang="scss" scoped>

.card-head {
  font-size: 16px;
  font-weight: bold;
  color: #000000;
}
.card-head::after {
  content: '';
  display: block;
  width: 50px;
  height: 2px;
  background-color: #000000;
  margin-top: 5px;
  margin-bottom: 20px;
}

.device-summary {
  margin-bottom: 32px;
  padding: 12px;
  padding-bottom: 32px;

  .message-item {
    display: flex;
    justify-content: center;
    align-items: flex-end;
  }

  .device-summary-head {
    font-size: 16px;
    font-weight: bold;
    color: #000000;
  }
  .split-line {
    display: inline-block;
    padding-right: 30px;
    span {
      font-size: 32px;
      font-weight: bold;
      color: #000000;
    }
  }
  .online-device {
    display: inline-block;
    .head {
      font-size: 16px;
      color: #5C9EFF;
      padding-bottom: 10px;
    }
    .body {
      font-size: 32px;
      font-weight: bold;
      color: #5C9EFF;
    }
  }
  .total-device {
    display: inline-block;
    .body {
      font-size: 24px;
      font-weight: bold;
      color: #172B4D;
    }
  }
  .package-count {
    .head {
      font-size: 16px;
      color: #172B4D;
      padding-bottom: 10px;
    }
    .body {
      font-size: 32px;
      font-weight: bold;
      color: #172B4D;
    }
  }
  .split-line {
    font-size: 24px;
    font-weight: bold;
    color: #172B4D;
  }
}

.device-kind {
  margin-bottom: 32px;
  padding: 12px;
  padding-bottom: 32px;
}

.device-chart {
  height: 278px;

  div {
    display: flex;
    justify-content: center;
  }
}

</style>
