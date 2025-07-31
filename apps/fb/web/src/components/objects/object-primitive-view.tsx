import { Button, Checkbox, Typography } from 'antd'
import { TPayloadData } from '../../store/main-api/generate/api'
import { DateTime } from 'luxon'
import _ from 'lodash'
import { DownloadOutlined } from '@ant-design/icons'

const { Text } = Typography

export function PropertyByTypeView({
  data,
}: {
  data: TPayloadData
}): React.ReactElement {
  switch (data.type) {
    case 'STR':
      return <Text strong>{data.values.join(', ')}</Text>
    case 'NUMBER':
      return <Text strong>{data.values.join(', ')}</Text>
    case 'DATE':
      return (
        <Text strong>
          {data.values
            .map((item) =>
              DateTime.fromISO(item).toLocaleString(
                DateTime.DATETIME_FULL_WITH_SECONDS
              )
            )
            .join(', ')}
        </Text>
      )
    case 'BOOL':
      return <Checkbox checked={_.first(data.values)} disabled />
    case 'FILE':
      return (
        <>
          {data.values.map((fileId, index) => (
            <Button
              type="link"
              href={`/api/v1/files/${fileId}`}
              key={index}
              icon={<DownloadOutlined />}
            >
              {index + 1} файл
            </Button>
          ))}
        </>
      )
    default:
      break
  }
  return <div>not found type: ${data.type}</div>
}
