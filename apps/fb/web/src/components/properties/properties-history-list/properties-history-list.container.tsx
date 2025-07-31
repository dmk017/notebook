import { Spin } from 'antd'
import { useGetPropertyHistoryApiV1PropertiesIdHistoryGetQuery } from '../../../store/main-api/generate/api'
import { PropertiesHistoryListView } from './properties-history-list.view'

interface PropertiesHistoryListContainerProps {
  id: string
}

export function PropertiesHistoryListContainer({
  id,
}: PropertiesHistoryListContainerProps): React.ReactElement {
  const state = useGetPropertyHistoryApiV1PropertiesIdHistoryGetQuery({
    id,
  })

  if (state.isLoading || state.data == null) {
    return <Spin />
  }

  return <PropertiesHistoryListView data={state.data} />
}
