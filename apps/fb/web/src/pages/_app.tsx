import '../public/antd.min.css'
import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { Provider } from 'react-redux'

import withTheme from '../theme'
import { ConfigProvider } from 'antd'
import ruRU from 'antd/locale/ru_RU'
import { store } from '../store'
import { AuthUserProvider } from '../providers/auth-user.provider'

export default function App({ Component, pageProps }: AppProps) {
  return withTheme(
    <Provider store={store}>
      <AuthUserProvider>
        <ConfigProvider locale={ruRU}>
          <Component {...pageProps} />
        </ConfigProvider>
      </AuthUserProvider>
    </Provider>
  )
}
