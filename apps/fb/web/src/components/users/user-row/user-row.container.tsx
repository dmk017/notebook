import { Skeleton } from 'antd'
import { useGetUserByIdApiV1UsersUserIdGetQuery } from '../../../store/admin-api/generate/api'
import { UserRowView } from './user-row.view'

interface UserRowProps {
  userId: string
}

export function UserRow({ userId }: UserRowProps): React.ReactElement {
  const state = useGetUserByIdApiV1UsersUserIdGetQuery({
    userId,
  })

  if (state.isLoading || state.data == null) {
    return <Skeleton.Input />
  }

  return <UserRowView user={state.data} />
}
