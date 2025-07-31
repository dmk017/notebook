import { useRouter } from 'next/router'
import { ModelsFormView } from './models-form.view'
import {
  useDeleteModelApiV1ModelsIdDeleteMutation,
  useGetModelByIdApiV1ModelsIdGetQuery,
  useUpdateModelApiV1ModelsIdPutMutation,
} from '../../../store/main-api/generate/api'
import { ModelPayloadType } from '../models.type'
import {
  Button,
  Divider,
  Flex,
  notification,
  Popconfirm,
  Spin,
  Typography,
} from 'antd'
import { RootRoutingPath } from '../../../routes'
import { DeleteOutlined } from '@ant-design/icons'
import { useResponsive } from '../../../hooks/use-responsive.hook'

const { Title } = Typography

interface ModelsUpdateFromProps {
  id: string
}

export function ModelsUpdateFrom(
  props: ModelsUpdateFromProps
): React.ReactElement {
  const { id } = props

  const { isMobile } = useResponsive()
  const router = useRouter()
  const state = useGetModelByIdApiV1ModelsIdGetQuery(
    {
      id,
    },
    {
      refetchOnMountOrArgChange: true,
    }
  )

  const [updateModel] = useUpdateModelApiV1ModelsIdPutMutation()
  const [deleteModel] = useDeleteModelApiV1ModelsIdDeleteMutation()

  async function handleClickUpdateProperty(
    data: ModelPayloadType
  ): Promise<void> {
    try {
      await updateModel({
        id,
        srcModelsModelsRouterApiSchemaPayload: data,
      }).unwrap()
      notification.success({
        message: 'Успех',
        description: 'Модель успешно обновлена',
        onClose: () => {
          router.push(RootRoutingPath.MODELS, undefined, { shallow: true })
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
      await deleteModel({
        id,
      }).unwrap()
      notification.success({
        message: 'Успех',
        description: 'Модель успешно обновлена',
        onClose: () => state.refetch(),
        showProgress: true,
        pauseOnHover: false,
      })
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
          <Title level={3}>Изменение модели</Title>
        </div>
        <div>
          <Popconfirm
            title="Предупреждение"
            description="Вы уверены что хотите удалить модель?"
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
      <ModelsFormView
        initValues={{
          ...state.data,
          properties: state.data.properties.map((property) => ({
            id: property.payload._id ?? '',
            is_required: property.is_required ?? false,
          })),
        }}
        onSubmit={handleClickUpdateProperty}
        isUpdate
      />
    </div>
  )
}
