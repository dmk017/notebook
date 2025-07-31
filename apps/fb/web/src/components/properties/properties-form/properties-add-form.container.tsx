import { Divider, Typography, notification } from 'antd'
import { useAddPropertyApiV1PropertiesPostMutation } from '../../../store/main-api/generate/api'
import { PropertiesFormView } from './properties-form.view'
import { PropertyPayloadType } from '../properties.type'
import { useRouter } from 'next/router'
import { RootRoutingPath } from '../../../routes'
import { ErrorResponseType } from '../../../store/api.types'

const { Title } = Typography

export function PropertiesAddForm(): React.ReactElement {
  const router = useRouter()
  const [addProperty] = useAddPropertyApiV1PropertiesPostMutation()

  async function handleClickCreateProperty(
    data: PropertyPayloadType
  ): Promise<void> {
    try {
      await addProperty({
        srcPropertiesPropertiesRouterApiSchemaPayload: data,
      }).unwrap()
      notification.success({
        message: 'Успех',
        description: 'Пользовательский тип успешно обновлен',
        onClose: () => {
          router.push(RootRoutingPath.PROPERTIES, undefined, {
            shallow: true,
            unstable_skipClientCache: true,
          })
        },
        showProgress: true,
        pauseOnHover: false,
      })
    } catch (error: unknown) {
      console.log(error)
      notification.error({
        message: 'Ошибка',
        description: (error as ErrorResponseType).data.detail,
      })
    }
  }

  return (
    <div>
      <Title level={2}>Создание пользовательского типа</Title>
      <Divider dashed></Divider>
      <PropertiesFormView onSubmit={handleClickCreateProperty} />
    </div>
  )
}
