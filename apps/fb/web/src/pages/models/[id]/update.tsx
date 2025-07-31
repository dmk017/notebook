import { Space } from 'antd'
import { LayoutConainer } from '../../../components/layout/layout.view'
import { ModelsUpdateFrom } from '../../../components/models/models-form/models-update-form.container'
import { useRouter } from 'next/router'
import _ from 'lodash'
import { AuthRoleProvider } from '../../../providers/auth-role.provider'

export default function ObjectsUpdatePage() {
  const router = useRouter()
  const modelId =
    router.query.id instanceof Array
      ? _.first(router.query.id)
      : router.query.id
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <Space direction="vertical" size={70} style={{ display: 'flex' }}>
          <ModelsUpdateFrom id={modelId ?? ''} />
        </Space>
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
