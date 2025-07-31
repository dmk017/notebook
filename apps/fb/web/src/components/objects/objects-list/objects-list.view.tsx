import {
  Button,
  Modal,
  Popconfirm,
  Tooltip,
  Space,
  Table,
  TableProps,
  Tag,
} from 'antd'
import { ColumnsType, TableRowSelection } from 'antd/es/table/interface'
import { useState } from 'react'
import { ObjectType } from '../objects.type'
import { PaginationType } from './pagination.type'
import { Objects } from '../../../store/main-api/generate/api'
import { DateTime } from 'luxon'
import {
  CheckCircleOutlined,
  CloseCircleOutlined,
  FileExcelOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons'
import { ModelRow } from '../../models/model-row/model-row.container'
import _ from 'lodash'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { ObjectCard } from '../object-card/object-card.container'
import { UserRow } from '../../users/user-row/user-row.container'
import { AntdColorProvider } from '../../ui-kit/antd/color-provider'

interface ObjectsListViewProps {
  data: Objects[]
  isLoading: boolean

  total: number

  paginationParams: PaginationType
  setPagination: (value: PaginationType) => void

  onApproveObjects: (ids: string[]) => void
  onDeclineObjects: (ids: string[]) => void

  onUploadObjectsFile: (ids: string[]) => void
}

export function ObjectsListView(
  props: ObjectsListViewProps
): React.ReactElement {
  const {
    data,
    isLoading,
    total,
    paginationParams,
    setPagination,
    onApproveObjects,
    onDeclineObjects,
    onUploadObjectsFile,
  } = props
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [showObjectId, setShowObjectId] = useState<string | null>(null)
  const { isMobile } = useResponsive()

  const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
    setSelectedRowKeys(newSelectedRowKeys)
  }
  const columns: ColumnsType<ObjectType> = [
    {
      title: 'Модель',
      dataIndex: 'model_id',
      width: '20%',
      render: (value) => <ModelRow modelId={value} />,
    },
    {
      title: 'Кто создал',
      dataIndex: 'owner_id',
      width: '20%',
      render: (value) => <UserRow userId={value} />,
    },
    {
      title: 'Дата создания',
      dataIndex: 'created_at',
      width: '20%',
      render: (value) =>
        DateTime.fromISO(value).toLocaleString(
          DateTime.DATETIME_MED_WITH_SECONDS
        ),
    },
    {
      title: 'Статус',
      dataIndex: 'status',
      render: (value: ObjectType['status']) => {
        if (value?.approve_at) {
          return (
            <Tooltip
              title={`${value.moderator_id} // ${DateTime.fromISO(
                value.approve_at
              ).toLocaleString(DateTime.DATETIME_MED_WITH_SECONDS)}`}
            >
              <Tag color="success">Подтвержден</Tag>
            </Tooltip>
          )
        }
        if (value?.decline_at) {
          return (
            <Tooltip
              title={`${value.moderator_id} // ${DateTime.fromISO(
                value.decline_at
              ).toLocaleString(DateTime.DATETIME_MED_WITH_SECONDS)}`}
            >
              <Tag color="error">Отклонен</Tag>
            </Tooltip>
          )
        }
        return <Tag color="warning">Ожидает</Tag>
      },
    },
    {
      title: 'Действия',
      key: 'operation',
      fixed: 'right',
      width: 150,
      render: (item: ObjectType) => (
        <Space>
          <Button
            shape="circle"
            icon={<InfoCircleOutlined />}
            onClick={() => setShowObjectId(item._id ?? '')}
          />
          <Button
            shape="circle"
            type="primary"
            icon={<CheckCircleOutlined />}
            onClick={() => onApproveObjects([item._id ?? ''])}
          />
          <Button
            shape="circle"
            type="dashed"
            danger
            icon={<CloseCircleOutlined />}
            onClick={() => onDeclineObjects([item._id ?? ''])}
          />
        </Space>
      ),
    },
  ]

  const rowSelection: TableRowSelection<ObjectType> = {
    selectedRowKeys,
    onChange: onSelectChange,
    selections: [
      Table.SELECTION_ALL,
      Table.SELECTION_INVERT,
      Table.SELECTION_NONE,
    ],
  }

  const handleTableChange: TableProps['onChange'] = (pagination) => {
    setPagination({
      page: pagination.current ?? 0,
      count: pagination.pageSize ?? 0,
    })
  }

  return (
    <div>
      <Table
        columns={columns}
        rowKey={(record) => record._id ?? ''}
        rowSelection={rowSelection}
        dataSource={data}
        pagination={{
          current: paginationParams.page,
          pageSize: paginationParams.count,
          total,
        }}
        scroll={{ x: isMobile ? 800 : 1500 }}
        loading={isLoading}
        onChange={handleTableChange}
      />
      {_.isEmpty(selectedRowKeys) ? null : (
        <Space
          direction={isMobile ? 'vertical' : 'horizontal'}
          style={{ display: 'flex' }}
        >
          <Popconfirm
            title="Подтверждение"
            description="Вы уверены что хотите подвердить все выбранные объекты?"
            onConfirm={() =>
              onApproveObjects(selectedRowKeys.map((item) => item.toString()))
            }
            okText="Да"
            cancelText="Нет"
          >
            <Button
              type="primary"
              disabled={_.isEmpty(selectedRowKeys)}
              block={isMobile}
            >
              Подтвердить выбранные
            </Button>
          </Popconfirm>
          <Popconfirm
            title="Подтверждение"
            description="Вы уверены что хотите отклонить все выбранные объекты?"
            onConfirm={() =>
              onDeclineObjects(selectedRowKeys.map((item) => item.toString()))
            }
            okText="Да"
            cancelText="Нет"
          >
            <Button
              danger
              disabled={_.isEmpty(selectedRowKeys)}
              block={isMobile}
            >
              Отклонить выбранные
            </Button>
          </Popconfirm>
          <AntdColorProvider color="#00b96b">
            <Popconfirm
              title="Подтверждение"
              description="Скачать выгрузку выбранных объектов?"
              onConfirm={() =>
                onUploadObjectsFile(
                  selectedRowKeys.map((item) => item.toString())
                )
              }
              okText="Да"
              cancelText="Нет"
            >
              <Button
                type="primary"
                block={isMobile}
                disabled={_.isEmpty(selectedRowKeys)}
                icon={<FileExcelOutlined />}
              >
                Скачать выбранные
              </Button>
            </Popconfirm>
          </AntdColorProvider>
        </Space>
      )}
      <Modal
        title="Подробный просмотр объекта"
        open={showObjectId != null}
        onOk={() => setShowObjectId(null)}
        onCancel={() => setShowObjectId(null)}
        cancelText="Назад"
        okText="ОК"
        width={isMobile ? undefined : 1000}
      >
        <ObjectCard objectId={showObjectId ?? ''} />
      </Modal>
    </div>
  )
}
