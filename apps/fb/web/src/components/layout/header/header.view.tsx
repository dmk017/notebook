import React, { useContext, useState } from 'react'
import { Button, Divider, Flex, Popover, Space, Tag, Typography } from 'antd'
import { headerStyles, headerContainerStyles } from './header.style'
import Link from 'next/link'
import { Collapse } from 'react-collapse'
import { MenuView } from '../menu'
import {
  CloseOutlined,
  LogoutOutlined,
  MenuOutlined,
  UserOutlined,
} from '@ant-design/icons'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { AuthUserContext } from '../../../providers/auth-user.provider'

const { Title } = Typography

export function HeaderView(): React.ReactElement {
  const { isMobile } = useResponsive()
  const [isOpenMenu, setOpenMenu] = useState(false)
  const { authUser } = useContext(AuthUserContext)
  return (
    <div style={headerContainerStyles}>
      <div style={headerStyles}>
        <Flex justify="space-between" align="center">
          <div>
            <Link href="/">
              <Title style={{ color: 'white', marginBottom: 0 }}>FORTUNA</Title>
            </Link>
          </div>
          <Space>
            <Popover
              content={
                <div>
                  <p>
                    Логин: <b>{authUser?.user_name}</b>
                  </p>
                  <Space>
                    Роль:
                    <Tag
                      color={
                        authUser?.role == 'ADMIN'
                          ? 'red'
                          : authUser?.role == 'MODERATOR'
                            ? 'warning'
                            : 'default'
                      }
                    >
                      {authUser?.role}
                    </Tag>
                  </Space>
                  <Divider dashed />
                  <a
                    href={`${process.env.LOGOUT_URI ?? '/404'}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Button type="link" danger icon={<LogoutOutlined />}>
                      Выход
                    </Button>
                  </a>
                </div>
              }
            >
              <Button
                type="text"
                size="large"
                icon={<UserOutlined style={{ color: 'white' }} />}
              />
            </Popover>
            {isMobile ? (
              <Button
                shape="circle"
                type="text"
                icon={
                  isOpenMenu ? (
                    <CloseOutlined style={{ color: 'white', fontSize: 30 }} />
                  ) : (
                    <MenuOutlined style={{ color: 'white', fontSize: 30 }} />
                  )
                }
                onClick={() => setOpenMenu((prev) => !prev)}
              />
            ) : null}
          </Space>
        </Flex>
      </div>
      {isMobile && (
        <Collapse isOpened={isOpenMenu}>
          <MenuView />
        </Collapse>
      )}
    </div>
  )
}
