import {
  Button,
  Col,
  DatePicker,
  Input,
  Popconfirm,
  Row,
  Select,
  SelectProps,
  Space,
  Tag,
} from 'antd'
import { useResponsive } from '../../../hooks/use-responsive.hook'
import { FileExcelOutlined, SearchOutlined } from '@ant-design/icons'
import { AntdColorProvider } from '../../ui-kit/antd/color-provider'
import { ModelsFilter } from './filters/models-filter'
import { UsersFilter } from './filters/users-filter'

const { RangePicker } = DatePicker

interface ObjectListFiltersViewProps {
  onModelSelect: (value: string[]) => void

  onUserSelect?: (value: string[]) => void

  onDatesSelect: (values: string[]) => void

  onStatusSelect: (values: string[]) => void

  onTextChange: (text: string) => void

  isEmptyFilters: boolean

  approved?: {
    onApprovedByFilter: () => void
    onDeclinedByFilter: () => void
  }

  downloaded?: {
    onDwnloadFile: () => void
  }
}

const options: SelectProps['options'] = [
  { label: 'Подтвержден', value: 'success' },
  { label: 'Отклонен', value: 'error' },
  { label: 'Ожидает', value: 'warning' },
]

const tagStatusMap: Record<string, string> = {
  success: 'approved',
  error: 'declined',
  warning: 'waiting',
}

export function ObjectListFiltersView(
  props: ObjectListFiltersViewProps
): React.ReactElement {
  const {
    onModelSelect,
    onUserSelect,
    onDatesSelect,
    onStatusSelect,
    onTextChange,
    isEmptyFilters,
    approved,
    downloaded,
  } = props
  const { isMobile } = useResponsive()
  return (
    <Row gutter={[16, 16]}>
      <Col xl={6} sm={24} xs={24}>
        <ModelsFilter onSelectValues={onModelSelect} />
      </Col>
      {onUserSelect == null ? null : (
        <Col xl={6} sm={24} xs={24}>
          <UsersFilter onSelectValues={onUserSelect} />
        </Col>
      )}
      <Col xl={6} sm={24} xs={24}>
        <RangePicker
          placeholder={['Дата создания', 'Дата окончания']}
          style={{ width: '100%' }}
          onChange={(values) => {
            onDatesSelect(
              values?.map((item) => item?.toISOString() ?? '') ?? []
            )
          }}
        />
      </Col>
      <Col xl={6} sm={24} xs={24}>
        <Select
          mode="multiple"
          placeholder="Статус объекта"
          style={{ width: '100%' }}
          maxCount={1}
          onChange={(values: string[]) => {
            onStatusSelect(values.map((key) => tagStatusMap[key]))
          }}
          tagRender={(props) => {
            const { label, value, closable, onClose } = props
            const onPreventMouseDown = (
              event: React.MouseEvent<HTMLSpanElement>
            ) => {
              event.preventDefault()
              event.stopPropagation()
            }
            return (
              <Tag
                color={value}
                onMouseDown={onPreventMouseDown}
                closable={closable}
                onClose={onClose}
                style={{ marginInlineEnd: 4 }}
              >
                {label}
              </Tag>
            )
          }}
          options={options}
        />
      </Col>
      <Col sm={24} xs={24}>
        <Input
          onChange={(e) => onTextChange(e.target.value)}
          size="large"
          placeholder="Введите ключевое слово"
          prefix={<SearchOutlined />}
        />
      </Col>
      {approved == null ? null : (
        <Col xl={8} sm={24} xs={24}>
          <Space
            direction={isMobile ? 'vertical' : 'horizontal'}
            style={{ display: 'flex' }}
          >
            <Popconfirm
              title="Подтверждение"
              description="Вы уверены что хотите подвердить все объекты по фильтрам?"
              onConfirm={approved.onApprovedByFilter}
              okText="Да"
              cancelText="Нет"
            >
              <Button type="primary" disabled={isEmptyFilters} block={isMobile}>
                Подтвердить по фильтрам
              </Button>
            </Popconfirm>
            <Popconfirm
              title="Подтверждение"
              description="Вы уверены что хотите отклонить все объекты по фильтрам?"
              onConfirm={approved.onDeclinedByFilter}
              okText="Да"
              cancelText="Нет"
            >
              <Button danger disabled={isEmptyFilters} block={isMobile}>
                Отклонить по фильтрам
              </Button>
            </Popconfirm>
          </Space>
        </Col>
      )}
      {downloaded == null ? null : (
        <Col xl={24} sm={24} xs={24}>
          <Space
            direction={isMobile ? 'vertical' : 'horizontal'}
            style={{ display: 'flex' }}
          >
            <AntdColorProvider color="#00b96b">
              <Popconfirm
                title="Подтверждение"
                description="Скачать выгрузку по объектов по фильтрам?"
                onConfirm={downloaded.onDwnloadFile}
                okText="Да"
                cancelText="Нет"
              >
                <Button
                  type="primary"
                  disabled={isEmptyFilters}
                  block={isMobile}
                  icon={<FileExcelOutlined />}
                >
                  Скачать выгрузку
                </Button>
              </Popconfirm>
            </AntdColorProvider>
          </Space>
        </Col>
      )}
    </Row>
  )
}
