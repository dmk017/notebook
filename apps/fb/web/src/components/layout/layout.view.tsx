import React from 'react'
import { HeaderContainer } from './header/header.container'
import { contentContainerStyle } from './layout.style'
import { Breadcrumb, Layout } from 'antd'
import { SiderView } from './sider/sider.view'
import { useResponsive } from '../../hooks/use-responsive.hook'

const { Content, Footer } = Layout

export const LayoutConainer: React.FC<{
  children: React.ReactElement
  breadcrumbs?: string[]
}> = ({ children, breadcrumbs = [] }) => {
  const { isMobile } = useResponsive()
  return (
    <Layout>
      <HeaderContainer />
      <Layout>
        {!isMobile && <SiderView />}
        <Content style={{ margin: isMobile ? 0 : 16 }}>
          {breadcrumbs.length > 0 && (
            <Breadcrumb style={{ margin: '16px 0' }}>
              {breadcrumbs.map((item, index) => (
                <Breadcrumb.Item key={index}>{item}</Breadcrumb.Item>
              ))}
            </Breadcrumb>
          )}
          <div style={contentContainerStyle}>{children}</div>
        </Content>
      </Layout>
      <Footer style={{ textAlign: 'center', height: 64 }}>
        Fortuna Bank ©2024
      </Footer>
    </Layout>
  )
}
