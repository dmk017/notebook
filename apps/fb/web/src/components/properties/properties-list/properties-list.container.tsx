import { Button, Divider, Flex, Space, Spin, Typography } from 'antd'
import { useRouter } from 'next/router'
import { useGetPropertiesApiV1PropertiesListPostMutation } from '../../../store/main-api/generate/api'
import { PropertiesListView } from './properties-list.view'
import { RootRoutingPath } from '../../../routes'
import { FormOutlined, HistoryOutlined } from '@ant-design/icons'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { useEffect } from 'react'

const { Title } = Typography

export function PropertiesListContainer(): React.ReactElement {
  const router = useRouter()
  const { isMobile } = useResponsive()
  const [fetch, state] = useGetPropertiesApiV1PropertiesListPostMutation()

  useEffect(() => {
    fetch({
      limit: Number.MAX_SAFE_INTEGER, // TODO: change after integrate pagination
      page: 1,
      propertyListFilters: {
        is_deleted: false,
      },
    })
  }, [fetch])

  function onClickUpdateProperty(id: string): void {
    router.push(`${RootRoutingPath.PROPERTIES}/${id}/update`)
  }

  function onClickHistoryProperty(id: string): void {
    router.push(`${RootRoutingPath.PROPERTIES}/${id}/history`)
  }

  if (state.isLoading || state.data == null) {
    return <Spin />
  }

  return (
    <div>
      <Flex justify="space-between" vertical={isMobile}>
        <div>
          <Title level={3}>Пользовательские типы данных</Title>
        </div>
        <Space>
          <Button
            type="primary"
            icon={<FormOutlined />}
            onClick={() => router.push(`/${RootRoutingPath.PROPERTIES}/add`)}
          >
            Добавить
          </Button>
          <Button
            type="dashed"
            icon={<HistoryOutlined />}
            onClick={() =>
              router.push(`/${RootRoutingPath.PROPERTIES}/archive`)
            }
          >
            Посмотреть архив
          </Button>
        </Space>
      </Flex>

      <Divider dashed></Divider>
      <PropertiesListView
        properties={state.data}
        onClickUpdatePropertyBtn={onClickUpdateProperty}
        onClickHistoryBtn={onClickHistoryProperty}
      />
    </div>
  )
}
