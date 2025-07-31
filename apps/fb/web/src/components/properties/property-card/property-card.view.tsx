import React from 'react'
import { Badge, Card, Space, Tooltip } from 'antd'
import {
  CheckSquareOutlined,
  EditOutlined,
  HistoryOutlined,
} from '@ant-design/icons'
import { propertyPrimitiveTypeMap } from '../properties.const'
import { PropertyType } from '../properties.type'
import {
  buttonPropertiesStyle,
  cardPropertiesStyle,
} from './property-card.style'
import _ from 'lodash'

interface PropertiesCardProps {
  data: PropertyType

  onClickUpdateBtn?: (id: string) => void
  onClickShowHistoryBtn?: (id: string) => void
  onClickRecovePropertyBtn?: (id: string) => void
}

export function PropertyCard(props: PropertiesCardProps): React.ReactElement {
  const {
    data,
    onClickUpdateBtn,
    onClickShowHistoryBtn,
    onClickRecovePropertyBtn,
  } = props
  return (
    <Card
      style={cardPropertiesStyle}
      title={data.name}
      actions={_.compact([
        onClickShowHistoryBtn == null ? null : (
          <Tooltip title="Показать историю">
            <HistoryOutlined
              style={buttonPropertiesStyle}
              key="history"
              onClick={() => onClickShowHistoryBtn(data._id ?? '')}
            />
          </Tooltip>
        ),
        onClickUpdateBtn == null ? null : (
          <Tooltip title="Изменение">
            <EditOutlined
              style={buttonPropertiesStyle}
              key="edit"
              onClick={() => onClickUpdateBtn(data._id ?? '')}
            />
          </Tooltip>
        ),
        onClickRecovePropertyBtn == null ? null : (
          <Tooltip title="Восстановление">
            <CheckSquareOutlined
              style={{
                ...buttonPropertiesStyle,
                color: '#228B22',
              }}
              key="recove"
              onClick={() => onClickRecovePropertyBtn(data._id ?? '')}
            />
          </Tooltip>
        ),
      ])}
    >
      {data.properties.map((field, index) => (
        <div key={index}>
          <Space>
            <div>{propertyPrimitiveTypeMap[field.primitive_type].icon}</div>
            <Badge title="обязательное" dot={field.is_required}>
              {field.is_multiple ? `[${field.name}]` : field.name}
            </Badge>
          </Space>
        </div>
      ))}
    </Card>
  )
}
