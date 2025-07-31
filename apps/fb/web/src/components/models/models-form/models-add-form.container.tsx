import { Divider, notification, Typography } from 'antd'
import { ModelsFormView } from './models-form.view'
import { useAddModelApiV1ModelsPostMutation } from '../../../store/main-api/generate/api'
import { useRouter } from 'next/router'
import { ModelPayloadType } from '../models.type'
import { RootRoutingPath } from '../../../routes'

const { Title } = Typography

export function ModelsAddFrom(): React.ReactElement {
  const router = useRouter()
  const [addModel] = useAddModelApiV1ModelsPostMutation()

  async function handleClickCreateModel(data: ModelPayloadType): Promise<void> {
    try {
      await addModel({
        srcModelsModelsRouterApiSchemaPayload: data,
      }).unwrap()
      notification.success({
        message: 'Успех',
        description: 'Модель успешно добавлена',
        onClose: () => {
          router.push(RootRoutingPath.MODELS, undefined, {
            shallow: true,
          })
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

  return (
    <div>
      <Title level={2}>Создание модели</Title>
      <Divider dashed></Divider>
      <ModelsFormView onSubmit={handleClickCreateModel} />
    </div>
  )
}
