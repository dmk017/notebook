import React from 'react'
import { containerStyles } from './container.style'

interface ContainerProps {
  children: React.ReactNode
  style?: React.CSSProperties
}

export function Container({
  children,
  style,
}: ContainerProps): React.ReactElement {
  return (
    <div
      style={{
        ...containerStyles,
        ...style,
      }}
    >
      {children}
    </div>
  )
}
