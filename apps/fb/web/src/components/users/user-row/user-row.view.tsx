import { Typography } from 'antd'
import { UserType } from '../types'
import Link from 'next/link'
import { RootRoutingPath } from '../../../routes'

interface UserRowProps {
  user: UserType
}

export function UserRowView({ user }: UserRowProps): React.ReactElement {
  return (
    <Link href={`${RootRoutingPath.USERS}/${user.id}`}>
      <Typography.Link>{user.username}</Typography.Link>
    </Link>
  )
}
