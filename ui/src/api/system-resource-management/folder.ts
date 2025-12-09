import { Result } from '@/request/Result'
import { get, post, del, put } from '@/request/index'
import { type Ref } from 'vue'

import useStore from '@/stores'
const prefix: any = { _value: '/workspace/' }
Object.defineProperty(prefix, 'value', {
  get: function () {
    const { user } = useStore()
    return this._value + user.getWorkspaceId()
  },
})

/**
 * 获得文件夹列表
 * @params 参数
 *  source : APPLICATION, KNOWLEDGE, TOOL
 *  data : {name: string}
 */
const getFolder: (
  source: string,
  data?: any,
  loading?: Ref<boolean>,
) => Promise<Result<Array<any>>> = (source, data, loading) => {
  return get(`${prefix.value}/${source}/folder`, data, loading)
}



export default {
  getFolder,

}
