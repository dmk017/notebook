import { Space } from 'antd'
import { LayoutConainer } from '../../../components/layout/layout.view'
import { PropertiesUpdateFrom } from '../../../components/properties/properties-form/properties-update-form.container'
import { useRouter } from 'next/router'
import _ from 'lodash'
import { AuthRoleProvider } from '../../../providers/auth-role.provider'

export default function PropertyUpdatePage() {
  const router = useRouter()
  const propertyId =
    router.query.id instanceof Array
      ? _.first(router.query.id)
      : router.query.id
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <Space direction="vertical" size={70} style={{ display: 'flex' }}>
          <PropertiesUpdateFrom id={propertyId ?? ''} />
        </Space>
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
