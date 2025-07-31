import { useRouter } from 'next/router'
import React from 'react'
import _ from 'lodash'
import { UserPage } from '../../../components/users/user-page/user-page.container'
import { Space } from 'antd'
import { LayoutConainer } from '../../../components/layout/layout.view'
import { AuthRoleProvider } from '../../../providers/auth-role.provider'

export default function UserIndexPage() {
  const router = useRouter()
  const userId =
    router.query.id instanceof Array
      ? _.first(router.query.id)
      : router.query.id
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <Space direction="vertical" size={70} style={{ display: 'flex' }}>
          <UserPage userId={userId ?? ''} />
        </Space>
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
