<template>
  <!-- one card for each device -->
  <div class="device-actuator-container">
    <el-row>
      <el-col v-for="device in actuatorDevices" :key="device.id" :xs="24" :sm="12" :md="8" :lg="6" :xl="6">
        <el-card shadow="hover" class="device-card">
          <span class="device-id">{{ device.did }}</span>
          <span class="device-name">{{ device.name }}</span>
          <el-button class="device-full" style="float: right; padding: 3px 0" type="text" icon="el-icon-full-screen" size="mini" @click="() => this.$router.push({ name: 'DeviceActuatorDetail', params: { id: device.id } })" />
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
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'DeviceActuator',
  data() {
    return {
      actuatorDevices: []
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
    }
  },
  mounted() {
    this.setData()
  },
  methods: {
    setData() {
      this.actuatorDevices = this.devices.filter(device => device.type === 1)
    }
  }
}
</script>

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
  margin: 10px 0;
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
