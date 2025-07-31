import React, { useState } from 'react'
import { Form, Divider, Button, Select, Input, Switch, Radio } from 'antd'
import {
  DeleteOutlined,
  CheckOutlined,
  CloseOutlined,
  PlusOutlined,
} from '@ant-design/icons'
import {
  propertyPrimitiveTypeMap,
  propertyValidationMap,
} from '../properties.const'

export function PropertyFormFields(): React.ReactElement {
  const [form] = Form.useForm()
  const [validationType, setValidationType] = useState('predefined')

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
                  name={[index, 'primitive_type']}
                  label="Тип данных"
                  layout="vertical"
                  rules={[
                    {
                      required: true,
                      message: 'Пожалуйста, введите Тип данных!',
                    },
                  ]}
                >
                  <Select
                    placeholder="Выберите тип данных"
                    allowClear
                    options={Object.entries(propertyPrimitiveTypeMap).map(
                      ([key, value]) => ({
                        value: key,
                        label: value.title,
                      })
                    )}
                    onChange={(value) =>
                      form.setFieldsValue({
                        properties: { [index]: { primitive_type: value } },
                      })
                    }
                  />
                </Form.Item>
                <Form.Item
                  label="Название"
                  layout="vertical"
                  name={[index, 'name']}
                  rules={[
                    {
                      required: true,
                      min: 2,
                      max: 99,
                      message: 'Пожалуйста, введите Название!',
                    },
                  ]}
                >
                  <Input placeholder="Название" />
                </Form.Item>
                {form.getFieldValue(['properties', index, 'primitive_type']) ===
                  'STR' ||
                form.getFieldValue(['properties', index, 'primitive_type']) ===
                  'NUMBER' ? (
                  <div>
                    <label>Валидация: </label>
                    <Radio.Group
                      onChange={(e) => setValidationType(e.target.value)}
                      value={validationType}
                    >
                      <Radio value="predefined">Выберите тип валидации</Radio>
                      <Radio value="custom">Ввести свой вариант</Radio>
                    </Radio.Group>

                    {validationType === 'predefined' && (
                      <Form.Item
                        name={[index, 'validation']}
                        layout="vertical"
                        label=""
                      >
                        <Select
                          placeholder="Выберите тип валидации"
                          allowClear
                          options={Object.entries(propertyValidationMap).map(
                            ([, value]) => ({
                              value: value.regex.source,
                              label: value.title,
                            })
                          )}
                        />
                      </Form.Item>
                    )}
                    {validationType === 'custom' && (
                      <Form.Item
                        name={[index, 'validation']}
                        layout="vertical"
                        label=""
                        rules={[
                          {
                            required: true,
                            message:
                              'Пожалуйста, введите регулярное выражение!',
                          },
                          {
                            validator: (_, value) => {
                              try {
                                new RegExp(value)
                                return Promise.resolve()
                              } catch (error) {
                                return Promise.reject(
                                  'Некорректное регулярное выражение!'
                                )
                              }
                            },
                          },
                        ]}
                      >
                        <Input placeholder="Регулярное выражение" />
                      </Form.Item>
                    )}
                  </div>
                ) : null}
                <Form.Item
                  name={[index, 'help_text']}
                  layout="vertical"
                  label="Подсказка"
                >
                  <Input placeholder="Подсказка" />
                </Form.Item>
                <Form.Item
                  name={[index, 'is_required']}
                  layout="vertical"
                  label="Обязательное"
                  valuePropName="checked"
                  initialValue={true}
                >
                  <Switch
                    checkedChildren={<CheckOutlined />}
                    unCheckedChildren={<CloseOutlined />}
                    defaultChecked
                  />
                </Form.Item>
                <Form.Item
                  name={[index, 'is_multiple']}
                  layout="vertical"
                  label="Множественное"
                  valuePropName="checked"
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
            <Form.Item style={{ display: 'flex', justifyContent: 'center' }}>
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
