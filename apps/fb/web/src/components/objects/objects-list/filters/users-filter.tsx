import { Select, Skeleton } from 'antd'
import _ from 'lodash'
import { ModelFilterProps } from './types'
import { useGetGroupByIdApiV1GroupsGroupIdAllGetQuery } from '../../../../store/admin-api/generate/api'
import { ROOT_GROUP_ID } from '../../../users/constant'

const USER_KEY_SEPARATOR = '|'

export function UsersFilter(props: ModelFilterProps): React.ReactElement {
  const { onSelectValues } = props
  const state = useGetGroupByIdApiV1GroupsGroupIdAllGetQuery({
    groupId: ROOT_GROUP_ID,
  })

  if (state.isLoading || state.data == null) {
    return <Skeleton.Input block />
  }

  return (
    <Select
      mode="multiple"
      allowClear
      placeholder="Выберите пользователя"
      style={{ width: '100%' }}
      onChange={(modelKeys: string[]) => {
        const userIds = _.compact(
          modelKeys.map((k) => _.first(_.split(k, USER_KEY_SEPARATOR, 2)))
        )
        onSelectValues(userIds)
      }}
      options={state.data.map((item) => ({
        label: item.username,
        value: _.join([item.id, item.username], USER_KEY_SEPARATOR),
      }))}
    />
  )
}
