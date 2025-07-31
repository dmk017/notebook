import { Space } from 'antd'
import { LayoutConainer } from '../../../components/layout/layout.view'
import { useRouter } from 'next/router'
import _ from 'lodash'
import { ModelCreateFrom } from '../../../components/models/model-create-form/model-create-form.container'

export default function ModelCreateObjectPage() {
  const router = useRouter()
  const modelId =
    router.query.id instanceof Array
      ? _.first(router.query.id)
      : router.query.id
  return (
    <LayoutConainer>
      <Space direction="vertical" size={70} style={{ display: 'flex' }}>
        <ModelCreateFrom modelId={modelId ?? ''} />
      </Space>
    </LayoutConainer>
  )
}
