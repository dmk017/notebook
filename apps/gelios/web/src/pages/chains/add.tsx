import { LayoutGeliosContainer } from "@/components/layout/layout.view"
import { BreadcrumbDataType } from "@/public/breadcrumb/breadcrumbType"
import { ChainsForm } from "@/components/chains/chainsForm/chainsAddForm"
import {
  CloudServerOutlined,
  ApartmentOutlined,
  PlusCircleOutlined 
} from '@ant-design/icons'

const addChainBreadcrumb: BreadcrumbDataType[] = [
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
        <PlusCircleOutlined  />
        <span>Добавление цепочки</span>
      </>
    )
  },
]
export default function ServerPage() {
  return (
    <LayoutGeliosContainer breadcrumbs={addChainBreadcrumb}>
      <ChainsForm />
    </LayoutGeliosContainer>
  )
}
