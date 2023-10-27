import { list } from '@/api/device'
import { getToken, removeToken } from '@/utils/auth'

const getDefaultState = () => {
  return {
    token: getToken(),
    devices: [],
    onlineDevices: [],
    sensors: [],
    actuators: [],
    onlineSensors: [],
    onlineActuators: []
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_DEVICES: (state, devices) => {
    state.devices = devices
    state.onlineDevices = devices.filter(device => device.status === 1)
    state.sensors = devices.filter(device => device.type === 0)
    state.actuators = devices.filter(device => device.type === 1)
    state.onlineSensors = devices.filter(device => device.type === 0 && device.status === 1)
    state.onlineActuators = devices.filter(device => device.type === 1 && device.status === 1)
  }
}

const actions = {
  // get devices
  list({ commit, state }) {
    return new Promise((resolve, reject) => {
      list(state.token).then(response => {
        const { data } = response
        if (!data) {
          reject('Verification failed, please Login again.')
        }
        // console.log(data)
        commit('SET_DEVICES', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

