import Link from 'next/link'
import { Layout, Space } from "antd";
import { headerStyles, titleStyles } from "./header.style";

const { Header } = Layout;

export function GeliosHeader(): React.ReactElement {
  return (
    <Header style={headerStyles}>
      <Space wrap size={16}>
        <Link href="/">
          <span style={titleStyles}>
            Gelios
          </span>
        </Link>
      </Space>
    </Header>
  )
}