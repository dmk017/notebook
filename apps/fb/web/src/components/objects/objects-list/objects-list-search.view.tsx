import {
  Divider,
  List,
  Button,
  Descriptions,
  Typography,
  Space,
  Flex,
} from 'antd'
import { Objects } from '../../../store/main-api/generate/api'
import { PropertyByTypeView } from '../object-primitive-view'
import { ModelRow } from '../../models/model-row/model-row.container'
import { UserRow } from '../../users/user-row/user-row.container'
import { useContext } from 'react'
import { AuthUserContext } from '../../../providers/auth-user.provider'

interface ObjectsListSearchViewProps {
  data: Objects[]
  isLoading: boolean
  nextFetch: () => void
  hasMore: boolean
}

export function ObjectsSearchResultView(
  props: ObjectsListSearchViewProps
): React.ReactElement {
  const { data, hasMore, isLoading, nextFetch } = props
  const { authUser } = useContext(AuthUserContext)
  return (
    <List
      dataSource={data}
      loading={isLoading}
      loadMore={
        hasMore ? (
          <Flex justify="center" style={{ margin: '16px 0' }}>
            <Button onClick={nextFetch}>Загрузить еще</Button>
          </Flex>
        ) : (
          <Divider plain>Пока на этом все</Divider>
        )
      }
      bordered
      renderItem={(item) => (
        <List.Item key={item._id}>
          <div style={{ width: '100%' }}>
            {item.payload.map((property, index) => (
              <div key={index} style={{ marginTop: index > 0 ? 16 : 0 }}>
                <Descriptions
                  title={
                    <Space direction="vertical">
                      <ModelRow modelId={item.model_id} />
                      <Space>
                        <Typography.Text>Модель: </Typography.Text>
                        <Typography.Text strong>
                          {property.property_name}
                        </Typography.Text>
                      </Space>
                      {authUser?.role == 'USER' ? null : (
                        <Space>
                          <Typography.Text>Добавил: </Typography.Text>
                          <UserRow userId={item.owner_id} />
                        </Space>
                      )}
                    </Space>
                  }
                  bordered
                  items={property.data.map((primitive) => ({
                    key: primitive.name,
                    label: primitive.name,
                    children: <PropertyByTypeView data={primitive} />,
                  }))}
                />
              </div>
            ))}
          </div>
        </List.Item>
      )}
    />
  )
}
