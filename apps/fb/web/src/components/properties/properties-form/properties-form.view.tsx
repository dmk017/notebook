import React from 'react'
import { Form, Button, Input, FormInstance } from 'antd'
import { PropertyFormFields } from './properties-form-fields.view'
import { PropertyPayloadType } from '../properties.type'

const SubmitButton = ({ form }: { form: FormInstance }) => {
  const [submittable, setSubmittable] = React.useState(false)
  const values = Form.useWatch([], form)

  React.useEffect(() => {
    form.validateFields({ validateOnly: true }).then(
      () => {
        setSubmittable(true)
      },
      () => {
        setSubmittable(false)
      }
    )
  }, [form, values])

  return (
    <Button type="primary" htmlType="submit" disabled={!submittable}>
      Сохранить
    </Button>
  )
}

interface PropertiesFromViewProps {
  initValues?: PropertyPayloadType
  isUpdate?: boolean
  onSubmit: (data: PropertyPayloadType) => void
}

export function PropertiesFormView(
  props: PropertiesFromViewProps
): React.ReactElement {
  const { initValues, onSubmit, isUpdate = false } = props
  const [form] = Form.useForm<PropertyPayloadType>()

  const handleFinish = (values: PropertyPayloadType): void => {
    onSubmit(values)
  }

  return (
    <Form<PropertyPayloadType>
      form={form}
      initialValues={initValues}
      onFinish={handleFinish}
      labelAlign="left"
    >
      <Form.Item
        name="name"
        label="Название"
        layout="vertical"
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
      <PropertyFormFields />
      <Form.Item style={{ display: 'flex', justifyContent: 'center' }}>
        <SubmitButton form={form} />
      </Form.Item>
    </Form>
  )
}
