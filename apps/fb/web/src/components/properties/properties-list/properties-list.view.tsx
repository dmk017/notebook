import React from 'react'
import { List } from 'antd'
import { PropertyCard } from '../property-card/property-card.view'
import { PropertyType } from '../properties.type'
import { useResponsive } from '../../../hooks/use-responsive.hook'

interface PropertiesListViewProps {
  properties: PropertyType[]

  onClickUpdatePropertyBtn?: (id: string) => void
  onClickRecovePropertyBtn?: (id: string) => void
  onClickHistoryBtn: (id: string) => void
}

export function PropertiesListView(
  props: PropertiesListViewProps
): React.ReactElement {
  const {
    properties,
    onClickUpdatePropertyBtn,
    onClickHistoryBtn,
    onClickRecovePropertyBtn,
  } = props
  const { isMobile } = useResponsive()
  return (
    <List<PropertyType>
      pagination={{
        onChange: (page) => {
          console.log(page)
        },
        pageSize: 12,
        position: 'bottom',
        align: 'start',
      }}
      grid={{
        gutter: 16,
        column: isMobile ? 1 : 4,
      }}
      dataSource={properties}
      renderItem={(item) => (
        <List.Item>
          <PropertyCard
            data={item}
            onClickUpdateBtn={onClickUpdatePropertyBtn}
            onClickShowHistoryBtn={onClickHistoryBtn}
            onClickRecovePropertyBtn={onClickRecovePropertyBtn}
          />
        </List.Item>
      )}
    />
  )
}
