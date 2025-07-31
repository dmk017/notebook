import { Space, Tabs, TabsProps, Typography } from 'antd'
import { ObjectType } from '../objects.type'
import { TPayloadData } from '../../../store/main-api/generate/api'
import { PropertyByTypeView } from '../object-primitive-view'

const { Text } = Typography

interface ObjectCardViewProps {
  object: ObjectType
}

function ObjectPropertyPayloadView({
  data,
}: {
  data: TPayloadData[]
}): React.ReactElement {
  return (
    <Space direction="vertical" style={{ display: 'flex' }}>
      {data.map((item, index) => {
        return (
          <Space key={index}>
            <Text>{item.name}</Text>: <PropertyByTypeView data={item} />
          </Space>
        )
      })}
    </Space>
  )
}

export function ObjectCardView({
  object,
}: ObjectCardViewProps): React.ReactElement {
  const items: TabsProps['items'] = object.payload.map((property, index) => {
    return {
      key: index.toString(),
      label: property.property_name,
      children: <ObjectPropertyPayloadView data={property.data} />,
    }
  })

  return <Tabs defaultActiveKey="2" items={items} />
}
