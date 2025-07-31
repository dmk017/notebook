import { LayoutGeliosContainer } from '@/components/layout/layout.view';
import { BreadcrumbDataType } from '@/public/breadcrumb/breadcrumbType';
import { ChainClientsData } from '@/components/chains/chainsClients/chainsClients.view';
import {CloudServerOutlined, ApartmentOutlined, UsergroupAddOutlined} from '@ant-design/icons'


const getChainClients: BreadcrumbDataType[] = [
  {
    href: '/',
    title: (
      <>
        <CloudServerOutlined />
        <span>Список серверов</span>
      </>)
  },
  {
    href: '/chains',
    title: (
      <>
        <ApartmentOutlined />
        <span>Список цепочек</span>
      </>
    ),
  },
  {
    title: (
      <>
        <UsergroupAddOutlined />
        <span>Клиенты цепочки</span>
      </>
    )
  },
]

export default function ServerInfoPage() {
  return (
    <LayoutGeliosContainer breadcrumbs={getChainClients}>
      <ChainClientsData />
    </LayoutGeliosContainer>
  )
}
