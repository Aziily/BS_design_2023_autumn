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
  }
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  background-color: rgb(240, 242, 245);
}
</style>
