import React, { useEffect } from 'react'
import { Form, Divider, Button, Select, Switch } from 'antd'
import {
  CheckOutlined,
  CloseOutlined,
  DeleteOutlined,
  PlusOutlined,
} from '@ant-design/icons'
import { btnAddStyle } from './models-form.style'
import { useGetPropertiesApiV1PropertiesListPostMutation } from '../../../store/main-api/generate/api'

export function ModelFieldsFormView(): React.ReactElement {
  const [fetch, state] = useGetPropertiesApiV1PropertiesListPostMutation()

  useEffect(() => {
    fetch({
      limit: Number.MAX_SAFE_INTEGER, // TODO: change after integrate pagination
      page: 1,
      propertyListFilters: {
        is_deleted: null,
      },
    })
  }, [fetch])

  return (
    <Form.List
      name="properties"
      rules={[
        {
          validator: async (_, fields) => {
            if (!fields) {
              return Promise.reject(new Error('Добавьте поле!'))
            }
          },
        },
      ]}
    >
      {(fields, { add, remove }) => {
        return (
          <div>
            {fields.map((field, index) => (
              <div key={field.key}>
                <Divider dashed></Divider>
                <Form.Item
                  name={[index, 'id']}
                  label="Тип данных"
                  rules={[
                    {
                      required: true,
                      message: 'Пожалуйста, введите Тип данных!',
                    },
                  ]}
                >
                  <Select
                    showSearch
                    loading={state.isLoading || state.data == null}
                    placeholder="Выберите тип данных"
                    allowClear
                    options={state.data?.map((item) => ({
                      value: item._id,
                      label: `${item.name}${item.deleted ? ` - удален` : ''}`,
                    }))}
                  />
                </Form.Item>
                <Form.Item
                  name={[index, 'is_required']}
                  label="Обязательное"
                  valuePropName="unchecked"
                  initialValue={false}
                >
                  <Switch
                    checkedChildren={<CheckOutlined />}
                    unCheckedChildren={<CloseOutlined />}
                  />
                </Form.Item>
                {fields.length > 1 ? (
                  <Button
                    type="primary"
                    className="dynamic-delete-button"
                    onClick={() => remove(field.name)}
                    icon={<DeleteOutlined />}
                    danger
                  >
                    Удалить поле
                  </Button>
                ) : null}
              </div>
            ))}
            <Divider />
            <Form.Item style={btnAddStyle}>
              <Button
                type="dashed"
                onClick={() => add()}
                icon={<PlusOutlined />}
              >
                Добавить поле
              </Button>
            </Form.Item>
          </div>
        )
      }}
    </Form.List>
  )
}
