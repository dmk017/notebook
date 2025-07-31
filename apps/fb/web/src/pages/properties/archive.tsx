import { LayoutConainer } from '../../components/layout/layout.view'
import { PropertiesArchiveListContainer } from '../../components/properties/properties-list/properties-archive-list.container'
import { AuthRoleProvider } from '../../providers/auth-role.provider'

export default function PropertiesArchivePage() {
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <PropertiesArchiveListContainer />
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
