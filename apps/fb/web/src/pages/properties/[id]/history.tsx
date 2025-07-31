import { Space } from 'antd'
import { LayoutConainer } from '../../../components/layout/layout.view'
import { useRouter } from 'next/router'
import _ from 'lodash'
import { PropertiesHistoryListContainer } from '../../../components/properties/properties-history-list/properties-history-list.container'
import { AuthRoleProvider } from '../../../providers/auth-role.provider'

export default function PropertyHistoryPage() {
  const router = useRouter()
  const propertyId =
    router.query.id instanceof Array
      ? _.first(router.query.id)
      : router.query.id
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <Space direction="vertical" size={70} style={{ display: 'flex' }}>
          <PropertiesHistoryListContainer id={propertyId ?? ''} />
        </Space>
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
