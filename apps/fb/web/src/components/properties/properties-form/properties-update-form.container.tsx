import {
  Button,
  Divider,
  Flex,
  notification,
  Popconfirm,
  Spin,
  Typography,
} from 'antd'
import {
  useDeletePropertyApiV1PropertiesIdDeleteMutation,
  useGetPropertyByIdApiV1PropertiesIdGetQuery,
  useUpdatePropertyApiV1PropertiesIdPutMutation,
} from '../../../store/main-api/generate/api'
import { PropertiesFormView } from './properties-form.view'
import { RootRoutingPath } from '../../../routes'
import { useRouter } from 'next/router'
import { PropertyPayloadType } from '../properties.type'
import { DeleteOutlined } from '@ant-design/icons'
import { useResponsive } from '../../../hooks/use-responsive.hook'

const { Title } = Typography

interface PropertiesUpdateFromProps {
  id: string
}

export function PropertiesUpdateFrom(
  props: PropertiesUpdateFromProps
): React.ReactElement {
  const { id } = props

  const { isMobile } = useResponsive()

  const router = useRouter()
  const state = useGetPropertyByIdApiV1PropertiesIdGetQuery({
    id,
  })

  const [updateProperty] = useUpdatePropertyApiV1PropertiesIdPutMutation()
  const [deleteProperty] = useDeletePropertyApiV1PropertiesIdDeleteMutation()

  async function handleClickUpdateProperty(
    data: PropertyPayloadType
  ): Promise<void> {
    try {
      await updateProperty({
        id,
        srcPropertiesPropertiesRouterApiSchemaPayload: data,
      }).unwrap()
      notification.success({
        message: 'Успех',
        description: 'Пользовательский тип успешно создан',
        onClose: () => {
          router.push(RootRoutingPath.PROPERTIES, undefined, { shallow: true })
        },
        showProgress: true,
        pauseOnHover: false,
      })
    } catch (error) {
      notification.error({
        message: 'Ошибка',
      })
    }
  }

  async function handleClickDeleteProperty(id: string): Promise<void> {
    try {
      await deleteProperty({
        id,
      }).unwrap()
      notification.success({
        message: 'Успех',
        description: 'Пользовательский тип успешно удален',
        showProgress: true,
        pauseOnHover: false,
      })
      state.refetch()
    } catch (error) {
      notification.error({
        message: 'Ошибка',
      })
    }
  }

  if (state.isLoading || state.data == null) {
    return <Spin />
  }

  return (
    <div>
      <Flex justify="space-between" vertical={isMobile}>
        <div>
          <Title level={3}>Изменение пользовательского типа</Title>
        </div>
        <div>
          <Popconfirm
            title="Предупреждение"
            description="Вы уверены что хотите удалить пользовательский тип?"
            onConfirm={() => handleClickDeleteProperty(id)}
          >
            <Button
              type="dashed"
              danger
              disabled={state.data.deleted}
              icon={<DeleteOutlined />}
            >
              {state.data.deleted ? 'Удален' : 'Удалить'}
            </Button>
          </Popconfirm>
        </div>
      </Flex>
      <Divider dashed></Divider>
      <PropertiesFormView
        onSubmit={handleClickUpdateProperty}
        initValues={state.data}
        isUpdate
      />
    </div>
  )
}
