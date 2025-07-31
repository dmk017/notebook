import { createContext, useMemo } from 'react'
import {
  useGetMeApiV1AuthMeGetQuery,
  User,
} from '../store/main-api/generate/api'

interface AuthUserProviderProps {
  children: React.ReactNode
}

interface AuthUserContext {
  authUser: User | null
}

export const AuthUserContext = createContext<AuthUserContext>({
  authUser: null,
})

export function AuthUserProvider({
  children,
}: AuthUserProviderProps): React.ReactElement {
  const state = useGetMeApiV1AuthMeGetQuery()

  const value = useMemo(
    () => ({
      authUser: state?.data ?? null,
    }),
    [state]
  )

  return (
    <AuthUserContext.Provider value={value}>
      {children}
    </AuthUserContext.Provider>
  )
}
