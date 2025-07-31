// import React from '../src/node_modules/@types/react'
import React from 'react'
import { ConfigProvider } from 'antd'
import { colors } from '../styles/colors'

const withTheme = (node: JSX.Element) => (
  <>
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: colors.background.primary,
        },
      }}
    >
      <ConfigProvider
        theme={{
          token: {
            borderRadius: 8,
          },
        }}
      >
        {node}
      </ConfigProvider>
    </ConfigProvider>
  </>
)

export default withTheme
