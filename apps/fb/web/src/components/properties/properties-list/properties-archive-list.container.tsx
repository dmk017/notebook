import {
  Alert,
  Button,
  Divider,
  Flex,
  notification,
  Spin,
  Typography,
} from 'antd'
import { useRouter } from 'next/router'
import { PropertiesListView } from './properties-list.view'
import { RootRoutingPath } from '../../../routes'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { IssuesCloseOutlined } from '@ant-design/icons'
import {
  useGetPropertiesApiV1PropertiesListPostMutation,
  useRecovePropertyApiV1PropertiesIdRecovePostMutation,
} from '../../../store/main-api/generate/api'
import { useEffect } from 'react'

const { Title } = Typography

export function PropertiesArchiveListContainer(): React.ReactElement {
  const router = useRouter()
  const { isMobile } = useResponsive()
  const [fetch, state] = useGetPropertiesApiV1PropertiesListPostMutation()

  const [recove] = useRecovePropertyApiV1PropertiesIdRecovePostMutation()

  useEffect(() => {
    fetch({
      limit: Number.MAX_SAFE_INTEGER, // TODO: change after integrate pagination
      page: 1,
      propertyListFilters: {
        is_deleted: true,
      },
    })
  }, [fetch])

  function handleCliclHistoryProperty(id: string): void {
    router.push(`${RootRoutingPath.PROPERTIES}/${id}/history`)
  }

  async function handleClickRecove(id: string): Promise<void> {
    try {
      await recove({
        id,
      })
      notification.success({
        message: 'Успех',
        description: 'Пользовательский тип успешно восстановлен',
        showProgress: true,
        pauseOnHover: false,
      })
      router.push(RootRoutingPath.PROPERTIES, undefined, {
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
          <Title level={3}>Удаленные пользовательские типы данных</Title>
        </div>
        <div>
          <Button
            type="dashed"
            icon={<IssuesCloseOutlined />}
            onClick={() => router.push(`/${RootRoutingPath.PROPERTIES}`)}
            block={isMobile}
          >
            Актуальный список
          </Button>
        </div>
      </Flex>
      <Alert
        message="В данном разделе представлены удаленные типы данных"
        type="warning"
        style={{ marginTop: 16 }}
      />
      <Divider dashed></Divider>
      <PropertiesListView
        properties={state.data}
        onClickHistoryBtn={handleCliclHistoryProperty}
        onClickRecovePropertyBtn={handleClickRecove}
      />
    </div>
  )
}
