import { Spin } from 'antd'
import React from 'react'
import { Container } from '../container'

export function SpinContainer(): React.ReactElement {
  return (
    <Container>
      <Spin size="large" />
    </Container>
  )
}
