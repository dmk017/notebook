import React, { useContext } from 'react'
import { Badge, Card, Space, Tooltip } from 'antd'
import { buttonStyle, cardStyle } from './model-card.style'
import { ModelType } from '../models.type'
import Link from 'next/link'
import { RootRoutingPath } from '../../../routes'
import { AntdIconProps } from '@ant-design/icons/lib/components/AntdIcon'
import { CloseCircleOutlined } from '@ant-design/icons'
import { AuthUserContext } from '../../../providers/auth-user.provider'

type ModelCardAction = {
  hint: string
  onClick: (id: string) => void
  Icon: React.FunctionComponent<
    Omit<AntdIconProps, 'ref'> & React.RefAttributes<HTMLSpanElement>
  >
}

interface ModelCardProps {
  data: ModelType
  actions: Array<ModelCardAction>
}

export function ModelCard(props: ModelCardProps): React.ReactElement {
  const { data, actions } = props
  const { authUser } = useContext(AuthUserContext)
  return (
    <Card
      style={cardStyle}
      title={data.name}
      actions={actions.map((action, index) => (
        <Tooltip title={action.hint} key={`action-btn-${index}`}>
          <action.Icon
            style={buttonStyle}
            onClick={() => action.onClick(data._id ?? '')}
          />
        </Tooltip>
      ))}
    >
      {data.properties.map((field, index) => {
        return (
          <div key={index}>
            <Space>
              {`${index + 1}.`}
              <Badge title="обязательное" dot={field.is_required}>
                {authUser?.role == 'ADMIN' ? (
                  <Link
                    href={`${RootRoutingPath.PROPERTIES}/${field.payload._id}`}
                  >
                    {field.payload.name}
                  </Link>
                ) : (
                  field.payload.name
                )}
              </Badge>
              {field.payload.deleted ? (
                <Tooltip title="Пользовательский тип удален">
                  <Badge
                    count={<CloseCircleOutlined style={{ color: '#f5222d' }} />}
                  />
                </Tooltip>
              ) : null}
            </Space>
          </div>
        )
      })}
    </Card>
  )
}
