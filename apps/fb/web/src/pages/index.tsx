import { Space } from 'antd'
import { LayoutConainer } from '../components/layout/layout.view'
import { ObjectsListSearch } from '../components/objects/objects-list/objects-list-search.container'

export default function HomePage() {
  return (
    <LayoutConainer>
      <Space direction="vertical" size={70} style={{ display: 'flex' }}>
        <ObjectsListSearch />
      </Space>
    </LayoutConainer>
  )
}
