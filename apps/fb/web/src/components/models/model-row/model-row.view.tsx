import { Space, Typography, Tag } from 'antd'
import { ModelType } from '../models.type'
import {
  CloseCircleOutlined,
  ExclamationCircleOutlined,
} from '@ant-design/icons'

const { Text } = Typography

interface ModelRowViewProps {
  model: ModelType
}

export function ModelRowView(props: ModelRowViewProps): React.ReactElement {
  return (
    <Space>
      <Text>{props.model.name}</Text>
      {props.model.deleted ? (
        <Tag icon={<CloseCircleOutlined />} color="error">
          Удален
        </Tag>
      ) : null}
      {props.model.next_id != null ? (
        <Tag icon={<ExclamationCircleOutlined />} color="warning">
          устарел
        </Tag>
      ) : null}
    </Space>
  )
}
