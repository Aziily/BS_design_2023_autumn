<template>
  <div class="device-kind-container">
    <el-row>
      <span class="card-head">Device Kind</span>
    </el-row>
    <el-row>
      <div class="choose-box">
        <a href="#/device/sensor">
          <div class="choose">
            <img src="https://cdn-icons-png.flaticon.com/512/2540/2540201.png">
            <span>Sensor</span>
          </div>
        </a>
      </div>
      <div class="choose-box">
        <a href="#/device/actuator">
          <div class="choose">
            <img src="https://tse1-mm.cn.bing.net/th/id/OIP-C.S1l6laEgs_yJJK99gAbQpAHaHa?pid=ImgDet&rs=1">
            <span>Actuator</span>
          </div>
        </a>
      </div>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
.device-kind-container {
  margin: 32px;
  .card-head {
    font-size: 24px;
    font-weight: bold;
    color: #000000;
  }
  .card-head::after {
    content: '';
    display: block;
    width: 80px;
    height: 2px;
    background-color: #000000;
    margin-top: 5px;
    margin-bottom: 20px;
  }
  a {
    text-decoration: none;
    color: black;
  }
  img {
    width: 100px;
    height: 100px;
  }
  span {
    font-size: 16px;
  }
}

.choose-box {
  display: inline-block;
  margin: 32px;

  .choose {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    span {
      margin-top: 10px;
    }
  }
}

</style>
