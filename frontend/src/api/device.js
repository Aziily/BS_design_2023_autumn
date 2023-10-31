import request from '@/utils/request'

export function list(token) {
  return request({
    url: '/device/list',
    method: 'get',
    params: { token }
  })
}

export function info(token, did) {
  return request({
    url: '/device/info' + '/' + did,
    method: 'get',
    params: { token }
  })
}

export function data(token, did) {
  return request({
    url: '/device/data' + '/' + did,
    method: 'get',
    params: { token }
  })
}

export function add(token, data) {
  return request({
    url: '/device/add',
    method: 'post',
    params: { token },
    data
  })
}

export function update(token, data, did) {
  return request({
    url: '/device/update' + '/' + did,
    method: 'post',
    params: { token },
    data
  })
}

export function remove(token, did) {
  return request({
    url: '/device/delete' + '/' + did,
    method: 'post',
    params: { token }
  })
}

export function dataList(token, data) {
  return request({
    url: '/device/dataList',
    method: 'post',
    params: { token },
    data
  })
}

export function getDataYear() {
  return request({
    url: '/device/dataYearList',
    method: 'get'
  })
}
