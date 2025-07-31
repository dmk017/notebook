import { Space } from 'antd'
import { LayoutConainer } from '../../components/layout/layout.view'
import { ModelsListContainer } from '../../components/models/models-list/models-list.container'

export default function ModelsPage() {
  return (
    <LayoutConainer>
      <Space direction="vertical" size={70} style={{ display: 'flex' }}>
        <ModelsListContainer />
      </Space>
    </LayoutConainer>
  )
}
