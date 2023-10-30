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
