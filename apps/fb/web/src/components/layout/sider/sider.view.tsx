import { useState } from 'react'
import { Button, Layout } from 'antd'
import { MenuFoldOutlined, MenuUnfoldOutlined } from '@ant-design/icons'
import { MenuView } from '../menu'

const { Sider } = Layout

export function SiderView(): React.ReactElement {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <Sider
      trigger={null}
      collapsible
      collapsed={collapsed}
      style={{ background: '#FFF' }}
      width={'276px'}
    >
      <Button
        type="text"
        icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
        onClick={() => setCollapsed(!collapsed)}
        style={{
          height: 67,
        }}
        block
      />
      <MenuView collapsed={collapsed} />
    </Sider>
  )
}
