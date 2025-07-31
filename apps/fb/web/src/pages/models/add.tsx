import { Space } from 'antd'
import { LayoutConainer } from '../../components/layout/layout.view'
import { ModelsAddFrom } from '../../components/models/models-form/models-add-form.container'
import { AuthRoleProvider } from '../../providers/auth-role.provider'

export default function PropertiesAddPage() {
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <Space direction="vertical" size={70} style={{ display: 'flex' }}>
          <ModelsAddFrom />
        </Space>
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
