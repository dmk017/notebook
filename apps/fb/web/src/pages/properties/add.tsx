import { LayoutConainer } from '../../components/layout/layout.view'
import { PropertiesAddForm } from '../../components/properties/properties-form/properties-add-form.container'
import { AuthRoleProvider } from '../../providers/auth-role.provider'

export default function PropertiesAddPage() {
  return (
    <AuthRoleProvider roles={['ADMIN']}>
      <LayoutConainer>
        <PropertiesAddForm />
      </LayoutConainer>
    </AuthRoleProvider>
  )
}
