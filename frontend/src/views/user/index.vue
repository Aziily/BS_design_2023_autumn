<template>
  <div class="user-container">
    <el-col>

      <el-row v-if="role === 0" class="admin-user">
        <div class="card-head">
          <span>Admin User</span>
        </div>
        <el-col v-for="user in users.filter(user => user.role === 0)" :key="user.uid" :xs="24" :sm="12" :md="8" :lg="6" :xl="6">
          <el-card shadow="hover" class="user-card">
            <span class="user-head">{{ user.username }}</span>
            <el-button class="user-delete" style="float: right; padding: 3px 0" type="text" icon="el-icon-delete" size="mini" @click="handleDelete(user)" />
            <el-button class="user-edit" style="float: right; padding: 3px 0" type="text" icon="el-icon-edit" size="mini" @click="handleEdit(user)" />
            <div class="user-info">
              <div class="user-email">Email: {{ user.email }}</div>
              <div class="user-phone">Phone: {{ user.phone ? user.phone : 'N/A' }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row class="normal-user">
        <div class="card-head">
          <span>Normal User</span>
        </div>
        <el-col v-for="user in users.filter(user => user.role === 1)" :key="user.uid" :xs="24" :sm="12" :md="8" :lg="6" :xl="6">
          <el-card shadow="hover" class="user-card">
            <span class="user-head">{{ user.username }}</span>
            <el-button class="user-delete" style="float: right; padding: 3px 0" type="text" icon="el-icon-delete" size="mini" @click="handleDelete(user)" />
            <el-button class="user-edit" style="float: right; padding: 3px 0" type="text" icon="el-icon-edit" size="mini" @click="handleEdit(user)" />
            <div class="user-info">
              <div class="user-email">Email: {{ user.email }}</div>
              <div class="user-phone">Phone: {{ user.phone ? user.phone : 'N/A' }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

    </el-col>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { list, remove } from '@/api/user'
import { getToken } from '@/utils/auth'

export default {
  name: 'UserList',
  data() {
    return {
      users: []
    }
  },
  computed: {
    ...mapGetters(['role', 'name'])
  },
  mounted() {
    this.getUsers()
  },
  methods: {
    handleEdit(row) {
      if (row.username !== this.name && this.role !== 0) {
        // console.log('You can not edit this user!')
        this.$message({
          type: 'warning',
          message: 'You can not edit this user!'
        })
        return
      }
      this.$router.push({ name: 'UserEdit', params: { user: row }})
    },
    handleDelete(row) {
      if (row.username === 'admin' || row.username === this.name) {
        // console.log('You can not delete this user!')
        this.$message({
          type: 'warning',
          message: 'You can not delete this user!'
        })
        return
      } else {
        this.$confirm('Are you sure to delete this user?', 'Warning', {
          confirmButtonText: 'Confirm',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          remove(getToken(), row.uid).then(() => {
            this.$message({
              type: 'success',
              message: 'Delete user successfully!'
            })
            this.getUsers()
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: 'Delete user canceled!'
          })
        })
      }
    },
    getUsers() {
      list(getToken()).then(response => {
        this.users = response.data
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.user-container {
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

  .admin-user{
    margin-bottom: 64px;
  }
  .normal-user{
    margin-bottom: 32px;
  }

  .user-card {
    margin: 16px;
    .user-head {
      font-size: 16px;
      font-weight: bold;
      color: #000000;
    }
    .user-info {
      margin-top: 16px;
      font-size: 14px;
      color: #000000;
    }
    .user-email {
      margin: 12px 0px;
    }
    .user-phone {
      margin: 12px 0px;
    }
    .user-edit {
      margin: 0px 4px
    }
    .user-delete {
      margin: 0px 4px
    }
  }
}
</style>
