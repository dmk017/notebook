import { useEffect } from 'react'
import { useGetModelsApiV1ModelsListPostMutation } from '../../../../store/main-api/generate/api'
import { Select, Skeleton } from 'antd'
import _ from 'lodash'
import { ModelFilterProps } from './types'

const MODEL_KEY_SEPARATOR = '-'

export function ModelsFilter(props: ModelFilterProps): React.ReactElement {
  const { onSelectValues } = props
  const [modelFetch, modelsState] = useGetModelsApiV1ModelsListPostMutation()

  useEffect(() => {
    modelFetch({
      page: 1,
      limit: Number.MAX_SAFE_INTEGER,
      modelsListFilter: {
        is_deleted: null,
      },
    })
  }, [modelFetch])

  if (modelsState.isLoading || modelsState.data == null) {
    return <Skeleton.Input block />
  }

  return (
    <Select
      mode="multiple"
      allowClear
      placeholder="Выберите модель"
      style={{ width: '100%' }}
      onChange={(modelKeys: string[]) => {
        const modelIds = _.compact(
          modelKeys.map((k) => _.first(_.split(k, MODEL_KEY_SEPARATOR, 2)))
        )
        onSelectValues(modelIds)
      }}
      options={modelsState.data.data.map((item) => ({
        label: `${item.name}${item.deleted ? ` - удален` : ''}`,
        value: _.join([item._id, item.name], MODEL_KEY_SEPARATOR),
      }))}
    />
  )
}
