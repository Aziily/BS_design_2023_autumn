<template>
  <el-card class="box-card-component">
    <div>
      <el-amap
        ref="map"
        map-style="amap://styles/62009be025f187dd3eafe327d2e55b8e"
        :center="center"
        :zoom="zoom"
        class="amap-demo"
        @init="initMap"
        @click="clickMap"
        @zoomend="zoomchange"
      >
        <el-amap-control-hawk-eye :visible="visible" />
        <el-amap-marker v-for="(marker, index) in markers" :key="index" :position="marker.position" />
        <el-amap-control-geolocation :visible="visible" position="RB" />
      </el-amap>
      <div v-if="center" class="address">
        <div>longitude: {{ center[0] }}</div>
        <div>latitude: {{ center[1] }}</div>
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'AddressMap',
  props: {
    origincenter: {
      type: Array,
      default: () => null
    }
  },
  data() {
    return {
      // 逆地理编码解析实例
      geocoder: null,
      visible: true,
      // 搜索关键字
      key: '',
      zoom: 15,
      markers: [],
      center: null
    }
  },
  mounted() {
    if (this.origincenter) {
      this.addPointer(this.origincenter)
    }
  },
  methods: {
    // init map
    initMap(e) {
      // const geocoder = new window.AMap.Geocoder()
      // this.geocoder = geocoder;
      return e
    },
    // click map
    clickMap(e) {
      this.addPointer([e.lnglat.lng, e.lnglat.lat])
    },
    // zoom change
    zoomchange(e) {
      this.zoom = e.target.getZoom()
    },
    // add pointer
    addPointer(position) {
      // set center
      this.center = position
      // set marker
      this.markers = [{
        position,
        id: Math.ceil(Math.random() * 1000)
      }]
      // set zoom
      this.zoom = this.zoom < 18 ? 18 : this.zoom
      // this.geocoder.getAddress(position, (status, result) => {
      //   if (status === 'complete' && result.info === 'OK') {
      //     this.address = result.regeocode.formattedAddress
      //   }
      // })
      // console.log(this.center)
      this.$emit('update:center', this.center)
    }
  }
}
</script>

<style scoped>
.amap-demo {
  height: 500px;
}
.address {
  top: 10px;
  left: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 5px;
  z-index: 100;
}
</style>
