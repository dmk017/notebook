import { LayoutConainer } from '../../components/layout/layout.view'
import { PropertiesListContainer } from '../../components/properties/properties-list/properties-list.container'
import { AuthRoleProvider } from '../../providers/auth-role.provider'

export default function PropertiesPage() {
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <PropertiesListContainer />
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
