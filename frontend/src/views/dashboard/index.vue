<template>
  <div class="dashboard-container">
    <component :is="currentRole" />
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'
import adminDashboard from './admin'

export default {
  name: 'Dashboard',
  components: { adminDashboard },
  data() {
    return {
      currentRole: 'adminDashboard'
    }
  },
  mounted() {
    this.$store.dispatch('user/getInfo').then(res => {
      this.$store.dispatch('device/list').then(res => {
        return
      })
    })
  }
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  background-color: rgb(240, 242, 245);
}
</style>
