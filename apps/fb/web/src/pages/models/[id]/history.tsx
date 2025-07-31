import { Space } from 'antd'
import { LayoutConainer } from '../../../components/layout/layout.view'
import { useRouter } from 'next/router'
import _ from 'lodash'
import { ModelsHistoryListContainer } from '../../../components/models/models-history-list/models-history-list.container'
import { AuthRoleProvider } from '../../../providers/auth-role.provider'

export default function ModelHistoryPage() {
  const router = useRouter()
  const modelId =
    router.query.id instanceof Array
      ? _.first(router.query.id)
      : router.query.id
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <Space direction="vertical" size={70} style={{ display: 'flex' }}>
          <ModelsHistoryListContainer id={modelId ?? ''} />
        </Space>
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
