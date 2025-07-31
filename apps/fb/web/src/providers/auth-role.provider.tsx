import { useContext, useEffect, useState } from 'react'
import { AuthUserContext } from './auth-user.provider'
import { User } from '../store/main-api/generate/api'
import _ from 'lodash'
import { useRouter } from 'next/router'

interface AuthRoleProviderProps {
  roles: User['role'][]
  children: React.ReactNode
}

export function AuthRoleProvider(
  props: AuthRoleProviderProps
): React.ReactElement {
  const router = useRouter()
  const { authUser } = useContext(AuthUserContext)
  const [allow, setAllow] = useState(false)

  useEffect(() => {
    if (!_.includes(props.roles, authUser?.role)) {
      router.push('/404')
    } else {
      setAllow(true)
    }
  }, [router, props.roles, authUser?.role])

  if (allow) return <>{props.children}</>

  return <></>
}
