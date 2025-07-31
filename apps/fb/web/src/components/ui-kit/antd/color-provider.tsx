import { ConfigProvider } from 'antd'

interface AntdColorProviderProps {
  children: React.ReactNode
  color: string
}

export function AntdColorProvider(
  props: AntdColorProviderProps
): React.ReactElement {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: props.color,
        },
      }}
    >
      {props.children}
    </ConfigProvider>
  )
}
