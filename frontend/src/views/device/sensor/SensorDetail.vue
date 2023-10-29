<template>
  <el-dialog title="Sensor Detail" :visible.sync="dialogVisible" width="30%">
    <el-form :model="form" label-width="80px">
      <el-form-item label="Device ID">
        <span>{{ form.did }}</span>
      </el-form-item>
      <el-form-item label="Device Name">
        <span>{{ form.name }}</span>
      </el-form-item>
      <el-form-item label="Device Description">
        <span>{{ form.description }}</span>
      </el-form-item>
      <el-form-item label="Device IP">
        <span>{{ form.ip }}</span>
      </el-form-item>
      <el-form-item label="Device Status">
        <span>{{ form.status }}</span>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">Close</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'SensorDetail',
  data() {
    return {
      dialogVisible: true,
      form: {
        did: '',
        name: '',
        description: '',
        ip: '',
        status: ''
      }
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
      this.form = this.devices.filter(device => device.did === this.$route.params.id)[0]
    }
  }
}
</script>
