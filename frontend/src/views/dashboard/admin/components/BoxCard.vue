<template>
  <el-card class="box-card-component">
    <div slot="header" class="box-card-header">
      <img src="https://wallpapercave.com/wp/wp6057449.jpg">
    </div>
    <div style="position:relative;">
      <pan-thumb :image="avatar" class="panThumb" />
      <!-- <mallki class-name="mallki-text" text="vue-element-admin" /> -->

      <div style="padding-top:50px;" class="info-item">
        <el-row>
          <span class="info-head">Name</span>
          <span>{{ name }}</span>
        </el-row>
      </div>
      <div class="info-item">
        <el-row>
          <span class="info-head">Role</span>
          <span>{{ role == 0 ? "Admin" : "User" }}</span>
        </el-row>
      </div>
      <div class="info-item">
        <el-row>
          <span class="info-head">EMail</span>
          <span>
            <a :href=" email ">{{ email }}</a>
          </span>
        </el-row>
      </div>
      <div class="info-item">
        <el-row>
          <span class="info-head">Phone</span>
          <span>{{ phone == "" ? "*" : phone }}</span>
        </el-row>
      </div>
      <div class="info-item">
        <el-row>
          <span class="info-head">Last Login</span>
          <span>{{ lastLogin }}</span>
        </el-row>
      </div>
      <div class="info-item">
        <el-row>
          <span class="info-head">Last IP</span>
          <span>{{ lastIP }}</span>
        </el-row>
      </div>

    </div>
  </el-card>
</template>

<script>
import { mapGetters } from 'vuex'
import PanThumb from '@/components/PanThumb'

export default {
  components: { PanThumb },

  computed: {
    ...mapGetters([
      'avatar',
      'name',
      'role',
      'email',
      'phone',
      'lastLogin',
      'lastIP'
    ])
  }
}
</script>

<style lang="scss" >
.box-card-component{
  .el-card__header {
    padding: 0px!important;
  }
}
</style>
<style lang="scss" scoped>
.box-card-component {
  .box-card-header {
    position: relative;
    height: 110px;
    img {
      width: 100%;
      height: 100%;
      transition: all 0.2s linear;
      &:hover {
        transform: scale(1.1, 1.1);
        filter: contrast(130%);
      }
    }
  }
  .mallki-text {
    position: absolute;
    top: 0px;
    right: 0px;
    font-size: 20px;
    font-weight: bold;
  }
  .panThumb {
    z-index: 100;
    height: 70px!important;
    width: 70px!important;
    position: absolute!important;
    top: -45px;
    left: 0px;
    border: 5px solid #ffffff;
    background-color: #fff;
    margin: auto;
    box-shadow: none!important;
    ::v-deep .pan-info {
      box-shadow: none!important;
    }
  }
  .info-item {
    width: 100%;
    margin-bottom: 20px;
    margin-left: 10px;
    font-size: 14px;
    .info-head { // fixed width
      display: inline-block;
      width: 80px;
      font-weight: bold;
      margin-right: 10px;
    }
  }
  @media only screen and (max-width: 1510px){
    .mallki-text{
      display: none;
    }
  }
}
</style>
