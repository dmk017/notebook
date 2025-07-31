import React from 'react'
import { List } from 'antd'
import {
  CheckSquareOutlined,
  EditOutlined,
  HistoryOutlined,
  PlusCircleOutlined,
} from '@ant-design/icons'
import { ModelType } from '../models.type'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { ModelCard } from '../model-card/model-card.view'
import _ from 'lodash'

interface ModelsListViewProps {
  models: ModelType[]

  onCreateObjectBtn?: (id: string) => void
  onClickUpdateBtn?: (id: string) => void
  onClickHistoryBtn?: (id: string) => void
  onClickRecoveBtn?: (id: string) => void
}

export function ModelsListView(props: ModelsListViewProps): React.ReactElement {
  const {
    models,
    onClickUpdateBtn,
    onClickHistoryBtn,
    onCreateObjectBtn,
    onClickRecoveBtn,
  } = props
  const { isMobile } = useResponsive()
  return (
    <List<ModelType>
      pagination={{
        onChange: (page) => {
          console.log(page)
        },
        pageSize: 12,
        position: 'bottom',
        align: 'start',
      }}
      grid={{
        gutter: 16,
        column: isMobile ? 1 : 4,
      }}
      dataSource={models}
      renderItem={(item) => (
        <List.Item>
          <ModelCard
            data={item}
            actions={_.compact([
              onClickUpdateBtn == null
                ? null
                : {
                    Icon: EditOutlined,
                    onClick: onClickUpdateBtn,
                    hint: 'Изменение',
                  },
              onClickHistoryBtn == null
                ? null
                : {
                    Icon: HistoryOutlined,
                    onClick: onClickHistoryBtn,
                    hint: 'История',
                  },
              onCreateObjectBtn == null
                ? null
                : {
                    Icon: PlusCircleOutlined,
                    onClick: onCreateObjectBtn,
                    hint: 'Создание объекта',
                  },
              onClickRecoveBtn == null
                ? null
                : {
                    Icon: CheckSquareOutlined,
                    onClick: onClickRecoveBtn,
                    hint: 'Восстановить',
                  },
            ])}
          />
        </List.Item>
      )}
    />
  )
}
