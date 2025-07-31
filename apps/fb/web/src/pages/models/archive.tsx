import { LayoutConainer } from '../../components/layout/layout.view'
import { ModelsArchiveListContainer } from '../../components/models/models-list/models-archive-list.container'
import { AuthRoleProvider } from '../../providers/auth-role.provider'

export default function ModelsArchivePage() {
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <ModelsArchiveListContainer />
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
