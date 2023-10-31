import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'get'
  })
}

export function list() {
  return request({
    url: '/user/list',
    method: 'get'
  })
}

export function update(token, data, uid) {
  return request({
    url: '/user/update/' + uid,
    method: 'post',
    params: { token },
    data
  })
}

export function remove(token, uid) {
  return request({
    url: '/user/delete/' + uid,
    method: 'post',
    params: { token }
  })
}

export function add(token, data) {
  return request({
    url: '/user/add',
    method: 'post',
    params: { token },
    data
  })
}
