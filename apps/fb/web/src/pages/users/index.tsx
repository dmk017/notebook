import { Space } from 'antd'
import { LayoutConainer } from '../../components/layout/layout.view'
import { GroupList } from '../../components/users/groups-list/groups-list.container'
import { AuthRoleProvider } from '../../providers/auth-role.provider'

export default function AuthorizePage() {
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <Space direction="vertical" size={70} style={{ display: 'flex' }}>
          <GroupList />
        </Space>
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
