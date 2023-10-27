<template>
  <el-col style="margin-left:8px;">
    <el-card class="device-summary-component">
      <el-col>
        <el-row>
          <span class="device-summary-head">Device Summary</span>
        </el-row>
        <!-- <el-row>{{ devices }}</el-row> -->
        <el-row>
          <el-col :span="12">
            <div class="online-device">
              <el-row><span class="head">Online</span></el-row>
              <el-row><span class="body">{{ onlineDevices.length }}</span></el-row>
            </div>
          </el-col>
          <el-col :span="6">
            <span class="split-line">/</span>
          </el-col>
          <el-col :span="12">
            <div class="total-device">
              <el-row><span class="head">Total</span></el-row>
              <el-row><span class="body">{{ devices.length }}</span></el-row>
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
          <el-col :span="12">
            <div class="sensor-device">
              <el-row><span class="head">Sensor</span></el-row>
              <el-row><div id="sensor-device"></div></el-row>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="actuator-device">
              <el-row><span class="head">Actuator</span></el-row>
              <el-row><div id="actuator-device"></div></el-row>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-card>

  </el-col>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      packageCount: 0
    }
  },
  computed: {
    ...mapGetters([
      'devices',
      'onlineDevices',
      'sensors',
      'actuators',
      'onlineSensors',
      'onlineActuators'
    ])
  }
  // ,
  // mounted() {
  //   this.drawSensorDevice()
  //   this.drawActuatorDevice()
  // },
  // methods: {
  //   drawSensorDevice() {
  //     var myChart = this.$echarts.init(document.getElementById('sensor-device'))
  //     var option = {
  //       title: {
  //         text: 'Sensor Device',
  //         left: 'center',
  //         top: 20,
  //         textStyle: {
  //           color: '#ccc'
  //         }
  //       },
  //       tooltip: {
  //         trigger: 'item',
  //         formatter: '{a} <br/>{b} : {c}'
  //       },
  //       series: [
  //         {
  //           name: 'Sensor Device',
  //           type: 'pie',
  //           radius: '55%',
  //           center: ['50%', '50%'],
  //           data: [
  //             { value: onlineSensors.length, name: 'Online' },
  //             { value: sensors.length - onlineSensors.length, name: 'Offline' }
  //           ],
  //           itemStyle: {
  //             emphasis: {
  //               shadowBlur: 10,
  //               shadowOffsetX: 0,
  //               shadowColor: 'rgba(0, 0, 0, .5)'
  //             }
  //           }
  //         }
  //       ]
  //     }
  //     myChart.setOption(option)
  //   },
  //   drawActuatorDevice() {
  //     var myChart = this.$echarts.init(document.getElementById('actuator-device'))
  //     var option = {
  //       title: {
  //         text: 'Actuator Device',
  //         left: 'center',
  //         top: 20,
  //         textStyle: {
  //           color: '#ccc'
  //         }
  //       },
  //       tooltip: {
  //         trigger: 'item',
  //         formatter: '{a} <br/>{b} : {c}'
  //       },
  //       series: [
  //         {
  //           name: 'Sensor Device',
  //           type: 'pie',
  //           radius: '55%',
  //           center: ['50%', '50%'],
  //           data: [
  //             { value: onlineActuators.length, name: 'Online' },
  //             { value: actuators.length - onlineActuators.length, name: 'Offline' }
  //           ],
  //           itemStyle: {
  //             emphasis: {
  //               shadowBlur: 10,
  //               shadowOffsetX: 0,
  //               shadowColor: 'rgba(0, 0, 0, .5)'
  //             }
  //           }
  //         }
  //       ]
  //     }
  //     myChart.setOption(option)
  //   }
  // }
}
</script>
