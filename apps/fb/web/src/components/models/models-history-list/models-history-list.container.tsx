import { Spin } from 'antd'
import { useGetModelHistoryApiV1ModelsIdHistoryGetQuery } from '../../../store/main-api/generate/api'
import { ModelsHistoryListView } from './models-history-list.view'

interface ModelsHistoryListContainerProps {
  id: string
}

export function ModelsHistoryListContainer({
  id,
}: ModelsHistoryListContainerProps): React.ReactElement {
  const state = useGetModelHistoryApiV1ModelsIdHistoryGetQuery({
    id,
  })

  if (state.isLoading || state.data == null) {
    return <Spin />
  }

  return <ModelsHistoryListView data={state.data} />
}
