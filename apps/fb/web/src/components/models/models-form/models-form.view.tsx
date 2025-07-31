import React from 'react'
import { Form, Input } from 'antd'
import { ModelFieldsFormView } from './models-form-fields.view'
import { btnAddStyle } from './models-form.style'
import { ModelPayloadType } from '../models.type'
import { SubmitButton } from './models-submit-form-btn'

interface ModelsFromViewProps {
  initValues?: ModelPayloadType
  isUpdate?: boolean
  onSubmit: (data: ModelPayloadType) => void
}

export function ModelsFormView(props: ModelsFromViewProps): React.ReactElement {
  const { initValues, isUpdate, onSubmit } = props
  const [form] = Form.useForm()

  const handleFinish = (values: ModelPayloadType): void => {
    onSubmit(values)
  }

  return (
    <Form<ModelPayloadType>
      form={form}
      initialValues={initValues}
      onFinish={handleFinish}
      labelAlign="left"
    >
      <Form.Item
        name="name"
        label="Название"
        rules={[
          {
            required: true,
            min: 2,
            max: 99,
            message: 'Пожалуйста, введите Название!',
          },
        ]}
      >
        <Input disabled={isUpdate} />
      </Form.Item>
      <ModelFieldsFormView />
      <Form.Item style={btnAddStyle}>
        <SubmitButton form={form} />
      </Form.Item>
    </Form>
  )
}
