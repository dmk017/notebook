import { Alert, List, Space, Typography } from 'antd'
import { PropertyType } from '../properties.type'
import { PropertyCard } from '../property-card/property-card.view'
import _ from 'lodash'
import { DateTime } from 'luxon'

const { Title, Text } = Typography

export interface PropertiesHistoryListViewProps {
  data: PropertyType[]
}

export function PropertiesHistoryListView(
  props: PropertiesHistoryListViewProps
): React.ReactElement {
  const { data } = props
  const actualProperty = _.find(data, (p) => p.next_id == null)
  return (
    <List
      header={
        <div>
          <Title level={3}>
            История изменения пользовательского типа - {actualProperty?.name}
          </Title>
          {actualProperty?.deleted ? (
            <Alert
              type="error"
              message="Этот пользовательский тип удален и с ним нельзя создать модель"
            />
          ) : (
            <></>
          )}
        </div>
      }
      grid={{ gutter: [16, 16], column: 1 }}
      dataSource={data}
      renderItem={(property, index) => (
        <Space direction="vertical" style={{ display: 'flex' }}>
          <Space>
            <Text>
              Дата изменения:{' '}
              <Text strong>
                {DateTime.fromISO(property.created_at ?? '', {
                  zone: 'utc',
                }).toLocaleString(DateTime.DATETIME_MED_WITH_SECONDS)}
              </Text>
            </Text>
            {property.next_id == null && <Text mark>Текущая версия</Text>}
          </Space>
          <PropertyCard data={property} key={index} />
        </Space>
      )}
    />
  )
}
