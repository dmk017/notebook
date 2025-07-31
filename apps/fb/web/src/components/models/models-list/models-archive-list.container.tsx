import {
  Alert,
  Button,
  Divider,
  Flex,
  notification,
  Spin,
  Typography,
} from 'antd'
import { ModelsListView } from './models-list.view'
import { useRouter } from 'next/router'
import { RootRoutingPath } from '../../../routes'
import {
  useGetModelsApiV1ModelsListPostMutation,
  useRecoveModelApiV1ModelsIdRecovePostMutation,
} from '../../../store/main-api/generate/api'
import { useEffect } from 'react'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { IssuesCloseOutlined } from '@ant-design/icons'

const { Title } = Typography

export function ModelsArchiveListContainer(): React.ReactElement {
  const router = useRouter()
  const { isMobile } = useResponsive()
  const [fetch, state] = useGetModelsApiV1ModelsListPostMutation()
  const [recove] = useRecoveModelApiV1ModelsIdRecovePostMutation()

  useEffect(() => {
    fetch({
      limit: Number.MAX_SAFE_INTEGER, // TODO: change after integrate pagination
      page: 1,
      modelsListFilter: {
        is_deleted: true,
      },
    })
  }, [fetch])

  function onClickHistoryProperty(id: string): void {
    router.push(`${RootRoutingPath.MODELS}/${id}/history`)
  }

  async function handleClickRecoveBtn(id: string): Promise<void> {
    try {
      await recove({
        id,
      })
      notification.success({
        message: 'Успех',
        description: 'Модель успешно восстановлена',
        showProgress: true,
        pauseOnHover: false,
      })
      router.push(RootRoutingPath.MODELS, undefined, {
        shallow: true,
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
          <Title level={3}>Удаленные модели</Title>
        </div>
        <div>
          <Button
            type="dashed"
            icon={<IssuesCloseOutlined />}
            onClick={() => router.push(`/${RootRoutingPath.MODELS}`)}
            block={isMobile}
          >
            Актуальный список
          </Button>
        </div>
      </Flex>
      <Alert
        message="В данном разделе представлены удаленные модели"
        type="warning"
        style={{
          marginTop: 16,
        }}
      />
      <Divider dashed></Divider>
      <ModelsListView
        models={state.data.data}
        onClickHistoryBtn={onClickHistoryProperty}
        onClickRecoveBtn={handleClickRecoveBtn}
      />
    </div>
  )
}
