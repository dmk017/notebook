import {CloudServerOutlined, EditOutlined} from '@ant-design/icons'
import { LayoutGeliosContainer } from '@/components/layout/layout.view';
import { BreadcrumbDataType } from '@/public/breadcrumb/breadcrumbType';
import { ChangeServersForm } from '@/components/servers/serversForms/serversChangeForm/serversChangeForm.view';

const changeServerBreadcrumb: BreadcrumbDataType[] = [
  {
    href: '/',
    title: (
      <>
        <CloudServerOutlined />
        <span>Список серверов</span>
      </>
    )
  },
  {
    title: (
      <>
        <EditOutlined />
        <span>Изменение сервера</span>
      </>
    )
  },
]

export default function ServerInfoPage() {
  return (
    <LayoutGeliosContainer breadcrumbs={changeServerBreadcrumb}>
      <ChangeServersForm />
    </LayoutGeliosContainer>
  )
}
