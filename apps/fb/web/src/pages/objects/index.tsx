import { Space } from 'antd'
import { LayoutConainer } from '../../components/layout/layout.view'
import { ObjectsList } from '../../components/objects/objects-list/objects-list.container'

export default function ModelsPage() {
  return (
    <LayoutConainer>
      <Space direction="vertical" size={70} style={{ display: 'flex' }}>
        <ObjectsList />
      </Space>
    </LayoutConainer>
  )
}
