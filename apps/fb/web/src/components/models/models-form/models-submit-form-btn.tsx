import React from 'react'
import { Form, Button, FormInstance } from 'antd'

interface SubmitButtonProps {
  form: FormInstance
  text?: string
}

export const SubmitButton = (props: SubmitButtonProps) => {
  const { form, text = 'Создать' } = props
  const [submittable, setSubmittable] = React.useState(false)

  // Watch all values
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
      {text}
    </Button>
  )
}
