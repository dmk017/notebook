import { Flex, Space, Spin, Switch } from 'antd'
import { useGetGroupByIdApiV1GroupsGroupIdGetQuery } from '../../../store/admin-api/generate/api'
import { ROOT_GROUP_ID } from '../constant'
import { GroupListTreeView } from './groups-list-tree.view'

import { Divider, Typography } from 'antd'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { useState } from 'react'
import { GroupListTableView } from './groups-list-table.view'
import router from 'next/router'
import { RootRoutingPath } from '../../../routes'

const { Title, Text } = Typography

export function GroupList(): React.ReactElement {
  const { isMobile } = useResponsive()
  const [treeMode, setTreeMode] = useState<boolean>(true)
  const state = useGetGroupByIdApiV1GroupsGroupIdGetQuery({
    groupId: ROOT_GROUP_ID,
  })

  function handleClickUser(userId: string) {
    router.push(`${RootRoutingPath.USERS}/${userId}`)
  }

  if (state.isLoading || state.data == null) {
    return <Spin />
  }

  return (
    <div>
      <Flex justify="space-between" vertical={isMobile}>
        <div>
          <Title level={3}>Список пользователей по ролям</Title>
        </div>
        <Space>
          <Text>Вид дерево</Text>
          <Switch
            checked={treeMode}
            onChange={() => setTreeMode((prev: boolean) => !prev)}
          />
        </Space>
      </Flex>

      <Divider dashed></Divider>
      {treeMode ? (
        <GroupListTreeView data={state.data} onClickUser={handleClickUser} />
      ) : (
        <GroupListTableView />
      )}
    </div>
  )
}
