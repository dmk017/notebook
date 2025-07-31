import { useState } from "react";
import type { MenuProps } from 'antd';
import { useRouter } from "next/router";
import { Layout, Button, Menu } from "antd";
import { siderStyles, buttonStyles, menuStyles } from "./sider.style";

import { 
  CloudServerOutlined,
  ApartmentOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined
 } from '@ant-design/icons'


type MenuItem = Required<MenuProps>['items'][number];
const { Sider } = Layout


function getItem(
  label: React.ReactNode,
  key: React.Key,
  icon?: React.ReactNode,
): MenuItem {
  return {
    key,
    icon,
    label,
  } as MenuItem;
}

const items: MenuItem[] = [
  getItem('Сервера', '/', <CloudServerOutlined />),
  getItem('Цепочки серверов', '/chains', <ApartmentOutlined />),
];

export function GeliosSider(): React.ReactElement {
  const [collapsed, setCollapsed] = useState<boolean>(false)
  const router = useRouter()
  const [currentLink, setCurrentLink] = useState<string>(router.asPath)

  function handleMenuItemClick(info: MenuItem): void {
    router.push(info?.key?.toString() ?? '')
    setCurrentLink(info?.key?.toString() ?? '');
  }

  return (
    <Sider
      trigger={null}
      collapsible
      collapsed={collapsed}
      style={siderStyles}
      width={'276px'}
    >
      <Button
        type="text"
        icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
        onClick={() => setCollapsed(!collapsed)}
        style={buttonStyles}
        block
      />
      <Menu 
        style={menuStyles}
        mode="inline"
        items={items}
        onClick={handleMenuItemClick}
        selectedKeys={[currentLink]}
      />
    </Sider>
  )
}