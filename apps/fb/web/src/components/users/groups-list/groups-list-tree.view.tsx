import { Tree } from 'antd'
import { GroupType } from '../types'
import { EventDataNode } from 'antd/es/tree'
import { Key, useState } from 'react'
import { useLazyGetGroupByIdApiV1GroupsGroupIdMembersGetQuery } from '../../../store/admin-api/generate/api'
import { UserOutlined } from '@ant-design/icons'
import _ from 'lodash'

interface GroupListViewProps {
  data: GroupType
  onClickUser: (userId: string) => void
}

interface DataNode {
  title: string
  key: string
  isLeaf?: boolean
  children?: DataNode[]
}

const updateTreeData = (
  list: DataNode[],
  key: React.Key,
  children: DataNode[]
): DataNode[] =>
  list.map((node) => {
    if (node.key === key) {
      return {
        ...node,
        children,
      }
    }
    if (node.children) {
      return {
        ...node,
        children: updateTreeData(node.children, key, children),
      }
    }
    return node
  })

export function GroupListTreeView(
  props: GroupListViewProps
): React.ReactElement {
  const { data, onClickUser } = props

  const initTreeData: DataNode[] = data.subGroups.map((group) => ({
    title: group.name,
    key: group.id,
  }))
  const [treeData, setTreeData] = useState(initTreeData)
  const [getGroup] = useLazyGetGroupByIdApiV1GroupsGroupIdMembersGetQuery()

  const onLoadData = ({ key, children }: EventDataNode<DataNode>) =>
    new Promise<void>((resolve, reject) => {
      if (children) {
        resolve()
        return
      }

      getGroup({
        groupId: key,
      })
        .then((payload) => {
          setTreeData((origin) =>
            updateTreeData(
              origin,
              key,
              payload.data?.map((user) => ({
                title: user.username,
                key: user.id,
                isLeaf: true,
                icon: <UserOutlined />,
              })) ?? []
            )
          )
        })
        .catch(reject)
      resolve()
    })

  function handleClickUser(
    selectedKeys: Key[],
    info: {
      node: EventDataNode<DataNode>
    }
  ) {
    const userId = _.first(selectedKeys)
    if (info.node.isLeaf) onClickUser(userId?.toString() ?? '')
  }

  return (
    <Tree
      showLine
      showIcon
      loadData={onLoadData}
      onSelect={handleClickUser}
      treeData={treeData}
    />
  )
}
