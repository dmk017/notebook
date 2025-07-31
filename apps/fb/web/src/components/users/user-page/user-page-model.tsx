import { useEffect } from 'react'
import {
  useGetModelsApiV1ModelsListPostMutation,
  useGetUserApiV1AuthUserIdGetQuery,
  useUpdateAccessModelsApiV1AuthModelsPutMutation,
} from '../../../store/main-api/generate/api'
import { Button, Form, notification, Select, Spin, Typography } from 'antd'
import { ModelType } from '../../models/models.type'

interface UserPageModelUpdaterProps {
  userId: string
}

export function UserPageModelUpdater({
  userId,
}: UserPageModelUpdaterProps): React.ReactElement {
  const state = useGetUserApiV1AuthUserIdGetQuery(
    {
      userId,
    },
    {
      refetchOnMountOrArgChange: true,
    }
  )
  const [fetch, stateModel] = useGetModelsApiV1ModelsListPostMutation()
  useEffect(() => {
    fetch({
      limit: Number.MAX_SAFE_INTEGER, // TODO: change after integrate pagination
      page: 1,
      modelsListFilter: {
        is_deleted: false,
      },
    })
  }, [fetch])

  const [updateUserModels] = useUpdateAccessModelsApiV1AuthModelsPutMutation()

  async function handleClickUpdateModel({
    modelNames,
  }: {
    modelNames: string[]
  }): Promise<void> {
    try {
      await updateUserModels({
        userId,
        accessModelNames: modelNames,
      }).unwrap()
      notification.success({
        message: 'Успех',
        description: 'Модели обновлены',
      })
      state.refetch()
    } catch (error) {
      notification.error({
        message: 'Ошибка',
        description: 'Не удалось обновить модели',
      })
    }
  }

  if (state.isLoading || state.data == null) {
    return <Spin />
  }

  const data: ModelType[] = stateModel.data?.data ?? []

  return (
    <div>
      <Typography.Title level={4}>Доступные модели</Typography.Title>
      <Form
        onFinish={handleClickUpdateModel}
        initialValues={{
          modelNames: state.data.access_model_names,
        }}
      >
        <Form.Item name="modelNames">
          <Select
            mode="multiple"
            size="large"
            placeholder="Выберите доступные модели"
            style={{ width: '100%' }}
            loading={stateModel.isLoading}
            options={
              data.map((model) => ({
                label: model.name,
                value: model.name,
              })) ?? []
            }
          />
        </Form.Item>
        <Form.Item shouldUpdate>
          {() => (
            <Button type="primary" htmlType="submit">
              Обновить
            </Button>
          )}
        </Form.Item>
      </Form>
    </div>
  )
}
