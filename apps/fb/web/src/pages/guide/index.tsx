import { Space } from 'antd'
import { LayoutConainer } from '../../components/layout/layout.view'

export default function GuidePage() {
  return (
    <LayoutConainer>
      <Space direction="vertical" size={70} style={{ display: 'flex' }}>
        <div>Guide</div>
      </Space>
    </LayoutConainer>
  )
}
