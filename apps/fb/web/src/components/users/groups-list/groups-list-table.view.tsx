import { Alert } from 'antd'
import { GroupType } from '../types'

export interface GroupListViewProps {
  data: GroupType
}

export function GroupListTableView(): React.ReactElement {
  return (
    <div>
      <Alert message={'Table mode soon? :)'} />
    </div>
  )
}
