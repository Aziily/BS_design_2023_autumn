<template>
  <div class="dashboard-editor-container">
    <github-corner class="github-corner" />

    <el-row :gutter="32" style="margin-bottom:32px;">
      <el-col :xs="{span: 20}" :sm="{span: 10}" :md="{span: 10}" :lg="{span: 5}" :xl="{span: 5}">
        <box-card />
      </el-col>
      <el-col :xs="{span: 20}" :sm="{span: 10}" :md="{span: 10}" :lg="{span: 5}" :xl="{span: 5}">
        <device-summary />
      </el-col>
    </el-row>

    <!-- <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>

    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <raddar-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <pie-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <bar-chart />
        </div>
      </el-col>
    </el-row> -->
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
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
