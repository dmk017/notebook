import { Flex, Divider, Typography } from 'antd'
import { UserType } from '../types'
import { UserPageModelUpdater } from './user-page-model'

interface UserPageViewProps {
  data: UserType
}

export function UserPageView(props: UserPageViewProps): React.ReactElement {
  const { data } = props
  return (
    <div>
      <Flex justify="space-between">
        <div>
          <Typography.Title level={3}>{data.username}</Typography.Title>
        </div>
      </Flex>

      <Divider dashed></Divider>
      <UserPageModelUpdater userId={data.id} />
    </div>
  )
}
