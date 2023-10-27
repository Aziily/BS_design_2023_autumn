import request from '@/utils/request'

export function list(token) {
  return request({
    url: '/device/list',
    method: 'get',
    params: { token }
  })
}
