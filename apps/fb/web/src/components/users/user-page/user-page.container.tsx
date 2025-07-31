import { Spin } from 'antd'
import { useGetUserByIdApiV1UsersUserIdGetQuery } from '../../../store/admin-api/generate/api'
import { UserPageView } from './user-page.view'

interface UserPageProps {
  userId: string
}

export function UserPage(props: UserPageProps): React.ReactElement {
  const { userId } = props

  const userState = useGetUserByIdApiV1UsersUserIdGetQuery({
    userId,
  })

  if (userState.isLoading || userState.data == null) {
    return <Spin />
  }

  return <UserPageView data={userState.data} />
}
