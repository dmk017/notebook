import React from 'react'

export type FontSizeType =
  | 'h0'
  | 'h1'
  | 'h2'
  | 'h3'
  | 'h4'
  | 'h5'
  | 'text1'
  | 'text2'
  | 'text3'
export type FontWeightType = 'light' | 'normal' | 'bold'

interface SizeProps {
  fontSize: Record<FontSizeType, React.CSSProperties['fontSize']>
  fontWeight: Record<FontWeightType, number>
}

export const sizes: SizeProps = {
  fontSize: {
    h0: '50px',
    h1: '40px',
    h2: '30px',
    h3: '24px',
    h4: '18px',
    h5: '16px',
    text1: '18px',
    text2: '16px',
    text3: '14px',
  },
  fontWeight: {
    light: 400,
    normal: 500,
    bold: 600,
  },
}
