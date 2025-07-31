import { LayoutGeliosContainer } from "@/components/layout/layout.view"
import { BreadcrumbDataType } from "@/public/breadcrumb/breadcrumbType"
import {CloudServerOutlined, PlusCircleOutlined } from '@ant-design/icons'
import { AddServersForm } from "@/components/servers/serversForms/serversAddForm/serversAddForm.view"

const addServerBreadcrumb: BreadcrumbDataType[] = [
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
        <PlusCircleOutlined  />
        <span>Добавление сервера</span>
      </>
    )
  },
];

export default function ServerInfoPage() {
  return (
    <LayoutGeliosContainer breadcrumbs={addServerBreadcrumb}>
      <AddServersForm />
    </LayoutGeliosContainer>
  )
}
