import { Alert, List, Space, Typography } from 'antd'
import _ from 'lodash'
import { DateTime } from 'luxon'
import { ModelCard } from '../model-card/model-card.view'
import { ModelType } from '../models.type'

const { Title, Text } = Typography

export interface ModelsHistoryListViewProps {
  data: ModelType[]
}

export function ModelsHistoryListView(
  props: ModelsHistoryListViewProps
): React.ReactElement {
  const { data } = props
  const actualModel = _.find(data, (m) => m.next_id == null)
  return (
    <List
      header={
        <div>
          <Title level={3}>
            История изменения модели типа - {_.first(data)?.name}
          </Title>
          {actualModel?.deleted ? (
            <Alert
              type="error"
              message="Эта модель удалена и по ней нельзя создать объект"
            />
          ) : (
            <></>
          )}
        </div>
      }
      grid={{ gutter: [16, 16], column: 1 }}
      dataSource={data}
      renderItem={(model, index) => (
        <Space direction="vertical" style={{ display: 'flex' }}>
          <Space>
            <Text>
              Дата изменения:{' '}
              <Text strong>
                {DateTime.fromISO(model.created_at ?? '', {
                  zone: 'utc',
                }).toLocaleString(DateTime.DATETIME_MED_WITH_SECONDS)}
              </Text>
            </Text>
            {model.next_id == null && <Text mark>Текущая версия</Text>}
          </Space>
          <ModelCard data={model} key={index} actions={[]} />
        </Space>
      )}
    />
  )
}
