import { Skeleton } from 'antd'
import { useGetModelByIdApiV1ModelsIdGetQuery } from '../../../store/main-api/generate/api'
import { ModelRowView } from './model-row.view'

export function ModelRow(props: { modelId: string }): React.ReactElement {
  const state = useGetModelByIdApiV1ModelsIdGetQuery({ id: props.modelId })

  if (state.isLoading || state.data == null) {
    return <Skeleton.Input />
  }

  return <ModelRowView model={state.data} />
}
