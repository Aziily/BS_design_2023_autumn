<template>
  <div class="amap-page-container">
    <el-card>
      <div slot="header" class="card-head">
        <span>Device Map</span>
      </div>
      <el-amap :center="center" :zoom="zoom" class="amap-block">
        <el-amap-control-geolocation @complete="getLocation" />
        <el-amap-marker
          v-for="device in devicesLocations"
          :key="device.did"
          :position="device.position"
          :title="device.title"
          :icon="device.icon"
        />
      </el-amap>
    </el-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data: function() {
    return {
      zoom: 15,
      center: [120.123051, 30.263896],
      devicesLocations: []
    }
  },
  computed: {
    ...mapGetters(['devices'])
  },
  watch: {
    devices: {
      handler: function(val, oldVal) {
        // console.log('devices: ', val)
        this.devicesLocations = val.map(device => {
          var description = device.description ? device.description : ''
          if (description.length > 20) {
            description = description.slice(0, 20) + '...'
          }
          return {
            did: device.did,
            position: [device.longitude, device.latitude],
            title: device.name + '\n' + 'Type: ' + (device.type === 0 ? 'sensor' : 'actuator') + '\n' + description,
            icon: device.type === 0 ? 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png' : 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png'
          }
        })
        // console.log('devicesLocations: ', this.devicesLocations)
      },
      deep: true
    }
  },
  mounted() {
    this.devicesLocations = this.devices.map(device => {
      var description = device.description ? device.description : ''
      if (description.length > 20) {
        description = description.slice(0, 20) + '...'
      }
      return {
        did: device.did,
        position: [device.longitude, device.latitude],
        title: device.name + '\n' + 'Type: ' + (device.type === 0 ? 'sensor' : 'actuator') + '\n' + description,
        icon: device.type === 0 ? 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png' : 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png'
      }
    })
    // console.log('devicesLocations: ', this.devicesLocations)
  },
  methods: {
    getLocation(e) {
      console.log('getLocation: ', e)
    },
    eventsHandler(e) {
      console.log('eventsHandler: ', e)
    }
  }
}
</script>

<style lang="scss" scoped>
.amap-page-container{
  height: 100%;

  .amap-block {
    height: 80vh;
  }
}
</style>
