import { Button, Divider, Flex, Space, Spin, Typography } from 'antd'
import { ModelsListView } from './models-list.view'
import { useRouter } from 'next/router'
import { RootRoutingPath } from '../../../routes'
import { useGetModelsApiV1ModelsListPostMutation } from '../../../store/main-api/generate/api'
import { useContext, useEffect } from 'react'
import { FormOutlined, HistoryOutlined } from '@ant-design/icons'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { AuthUserContext } from '../../../providers/auth-user.provider'

const { Title } = Typography

export function ModelsListContainer(): React.ReactElement {
  const router = useRouter()
  const [fetch, state] = useGetModelsApiV1ModelsListPostMutation()

  const { isMobile } = useResponsive()

  const { authUser } = useContext(AuthUserContext)

  useEffect(() => {
    fetch({
      limit: Number.MAX_SAFE_INTEGER, // TODO: change after integrate pagination
      page: 1,
      modelsListFilter: {
        is_deleted: false,
      },
    })
  }, [fetch])

  function onClickAddModelBtn(): void {
    router.push(`${RootRoutingPath.MODELS}/add`)
  }

  function onClickArchivedModelBtn(): void {
    router.push(`${RootRoutingPath.MODELS}/archive`)
  }

  function onClickUpdateProperty(id: string): void {
    router.push(`${RootRoutingPath.MODELS}/${id}/update`)
  }

  function onClickHistoryProperty(id: string): void {
    router.push(`${RootRoutingPath.MODELS}/${id}/history`)
  }

  function onClickCreateObject(id: string): void {
    router.push(`${RootRoutingPath.MODELS}/${id}/create`)
  }

  if (state.isLoading || state.data == null) {
    return <Spin />
  }

  return (
    <div>
      <Flex justify="space-between" vertical={isMobile}>
        <div>
          <Title level={3}>Доступные модели</Title>
        </div>
        {authUser?.role == 'ADMIN' ? (
          <Space>
            <Button
              type="primary"
              icon={<FormOutlined />}
              onClick={onClickAddModelBtn}
            >
              Добавить
            </Button>
            <Button
              type="dashed"
              icon={<HistoryOutlined />}
              onClick={onClickArchivedModelBtn}
            >
              Посмотреть архив
            </Button>
          </Space>
        ) : null}
      </Flex>
      <Divider dashed></Divider>
      <ModelsListView
        models={state.data.data}
        onClickHistoryBtn={
          authUser?.role == 'ADMIN' ? onClickHistoryProperty : undefined
        }
        onClickUpdateBtn={
          authUser?.role == 'ADMIN' ? onClickUpdateProperty : undefined
        }
        onCreateObjectBtn={onClickCreateObject}
      />
    </div>
  )
}
