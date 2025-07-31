import React from "react";
import { Breadcrumb, Layout } from "antd";
import { GeliosSider } from "./sider/sider.view";
import { GeliosHeader } from "./header/header.view";
import { BreadcrumbDataType } from "@/public/breadcrumb/breadcrumbType";
import { 
  layoutStyles, 
  contentStyles, 
  footerStyles, 
  breadcrumbsStyles 
} from "./layout.style";

const { Content, Footer } = Layout;


export const LayoutGeliosContainer: React.FC<
  {
    children: React.ReactElement,
    breadcrumbs?: BreadcrumbDataType[]
  }
> = ({children, breadcrumbs = []}) => {
  return (
    <Layout style={layoutStyles}>
      <GeliosHeader />
      <Layout>
        <GeliosSider />
        <Content style={contentStyles}>
          {breadcrumbs.length > 0 && (
            <Breadcrumb 
              items={breadcrumbs} 
              style={breadcrumbsStyles} 
            />
          )}
          {children}
        </Content>
      </Layout>
      <Footer style={footerStyles} />
    </Layout>
  )
}