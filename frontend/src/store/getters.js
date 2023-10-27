const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,

  avatar: state => state.user.avatar,
  name: state => state.user.name,
  email: state => state.user.email,
  phone: state => state.user.phone,
  role: state => state.user.role,
  lastLogin: state => state.user.lastLogin,
  lastIP: state => state.user.lastIP,

  devices: state => state.device.devices
}
export default getters
