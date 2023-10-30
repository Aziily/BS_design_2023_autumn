<template>
  <div class="dashboard-editor-container">
    <github-corner class="github-corner" />

    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :md="24" :lg="8" :xl="8" style="margin-bottom:32px;wdith:100%">
        <div class="box-wrapper">
          <box-card />
          <el-card style="margin-top: 32px;">
            <div display="flex" justify-content="center" style="margin-bottom: 16px;margin-top: 16px;" align="center">
              <img src="https://i0.wp.com/tinkercademy.com/wp-content/uploads/2018/04/python-icon.png" style="height: 80px;margin: 10px;">
              <img src="https://www.probytes.net/wp-content/uploads/2018/10/flask-logo-png-transparent-233x300.png" style="height: 80px;margin: 10px;">
              <img src="https://th.bing.com/th/id/OIP._IBVgzNUmjeZQOT6fhq2HQHaHa?pid=ImgDet&rs=1" style="height: 80px;margin: 10px;">
              <img src="https://wpimg.wallstcn.com/69a1c46c-eb1c-4b46-8bd4-e9e686ef5251.png" style="height: 80px;margin: 10px;">
            </div>
          </el-card>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :md="24" :lg="16" :xl="16">
        <device-summary />
      </el-col>
    </el-row>

  </div>
</template>

<script>
import GithubCorner from '@/components/GithubCorner'
import BoxCard from './components/BoxCard'
import DeviceSummary from './components/DeviceSummary'

export default {
  name: 'DashboardAdmin',
  components: {
    GithubCorner,
    BoxCard,
    DeviceSummary
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  height: 100%;
  padding: 32px;
  position: relative;
  background-color: rgb(240, 242, 245);
  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .box-wrapper {
    margin-left: 16px;
    margin-right: 16px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
