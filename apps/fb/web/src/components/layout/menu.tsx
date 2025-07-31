import {
  ApartmentOutlined,
  CheckSquareOutlined,
  LockOutlined,
  SearchOutlined,
  SettingOutlined,
  SolutionOutlined,
} from '@ant-design/icons'
import { Menu, type MenuProps } from 'antd'
import { RootRoutingPath } from '../../routes'
import { useRouter } from 'next/router'
import { useContext } from 'react'
import { AuthUserContext } from '../../providers/auth-user.provider'

export type MenuItem = Required<MenuProps>['items'][number]

function getItem(
  label: React.ReactNode,
  key: React.Key,
  icon?: React.ReactNode,
  children?: MenuItem[]
): MenuItem {
  return {
    key,
    icon,
    children,
    label,
  } as MenuItem
}

interface MenuViewProps {
  collapsed?: boolean
}

export function MenuView(props: MenuViewProps): React.ReactElement {
  const { collapsed = false } = props
  const router = useRouter()
  const { authUser } = useContext(AuthUserContext)

  function handleMenuItemClick(info: MenuItem): void {
    router.push(info?.key?.toString() ?? '')
  }

  const menuItems: MenuItem[] = [
    getItem('Главная', RootRoutingPath.HOME, <SearchOutlined />),
    authUser?.role == 'ADMIN'
      ? getItem('Мои объекты', RootRoutingPath.OBJECTS, <CheckSquareOutlined />)
      : null,
    getItem('Доступные модели', RootRoutingPath.MODELS, <ApartmentOutlined />),
    authUser?.role == 'ADMIN'
      ? getItem(
          'Пользовательские типы',
          RootRoutingPath.PROPERTIES,
          <SolutionOutlined />
        )
      : null,
    authUser?.role == 'ADMIN'
      ? getItem('Настройки', 'sub1', <SettingOutlined />, [
          getItem('Доступы', RootRoutingPath.USERS, <LockOutlined />),
        ])
      : null,
  ]

  return (
    <Menu
      style={{ height: '100%' }}
      defaultSelectedKeys={['/']}
      selectedKeys={[router.pathname]}
      mode="inline"
      items={menuItems}
      inlineCollapsed={collapsed}
      onClick={handleMenuItemClick}
    />
  )
}
