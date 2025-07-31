import { useEffect, useState } from 'react'
import {
  useApproveObjectsApiV1ObjectsApprovePutMutation,
  useDeclineObjectsApiV1ObjectsDeclinePutMutation,
  useGetCountObjectsApiV1ObjectsCountGetQuery,
  useObjectsSearchApiV1ObjectsSearchPostMutation,
} from '../../../store/main-api/generate/api'
import { ObjectsListView } from './objects-list.view'
import { Divider, notification, Typography } from 'antd'
import { ObjectListFiltersView } from './objects-list-filters.view'
import _ from 'lodash'
import { ObjectType, SearchObjectWithKey } from '../objects.type'
import { useDebouncedCallback } from 'use-debounce'
import { downloadObjectFile } from '../../../store/file-download-file'

const { Title } = Typography

const MODELS_FILTER_KEY = 'MODELS_FILTER'
const USERS_FILTER_KEY = 'USERS_FILTER'
const RANGE_FILTER_KEY = 'RANGE_FILTER'
const STATUS_FILTER_KEY = 'STATUS_FILTER'
const TEXT_FILTER_KEY = 'TEXT_FILTER'

export function ObjectsList(): React.ReactElement {
  const [data, setData] = useState<ObjectType[]>([])
  const debouncedText = useDebouncedCallback((value) => {
    handleTextChange(value)
  }, 500)
  const initPagination = {
    page: 1,
    count: 20,
  }
  const [searchParams, setSearchParams] = useState<SearchObjectWithKey>({
    text: undefined,
    ...initPagination,
    filters: [],
  })

  const [fetch, state] = useObjectsSearchApiV1ObjectsSearchPostMutation()

  const totalState = useGetCountObjectsApiV1ObjectsCountGetQuery({
    page: 1,
    limit: Number.MAX_SAFE_INTEGER,
  })

  const [approve] = useApproveObjectsApiV1ObjectsApprovePutMutation()
  const [decline] = useDeclineObjectsApiV1ObjectsDeclinePutMutation()

  useEffect(() => {
    fetch({
      searchObject: searchParams,
    }).catch()
  }, [fetch, searchParams])

  useEffect(() => {
    if (state.data == null) return
    setData((prev) => _.concat(prev, state.data?.data))
  }, [state])

  function handleModelSelect(modelIds: string[]): void {
    setData([])
    setSearchParams((prev) => {
      const filters = _.remove(
        prev.filters,
        (filter) => filter.key != MODELS_FILTER_KEY
      )
      if (_.isEmpty(modelIds)) {
        return {
          ...initPagination,
          filters,
        }
      }
      return {
        ...initPagination,
        filters: [
          ...filters,
          {
            type: 'group',
            group: 'OR',
            key: MODELS_FILTER_KEY,
            conditions: modelIds.map((value) => ({
              type: 'isolated',
              property: 'model_id',
              operator: 'eq',
              value,
            })),
          },
        ],
      }
    })
  }

  function handleUserSelect(userIds: string[]): void {
    setData([])
    setSearchParams((prev) => {
      const filters = _.remove(
        prev.filters,
        (filter) => filter.key != USERS_FILTER_KEY
      )
      if (_.isEmpty(userIds)) {
        return {
          ...initPagination,
          filters,
        }
      }
      return {
        ...initPagination,
        filters: [
          ...filters,
          {
            type: 'group',
            group: 'OR',
            key: USERS_FILTER_KEY,
            conditions: userIds.map((value) => ({
              type: 'isolated',
              property: 'owner_id',
              operator: 'eq',
              value,
            })),
          },
        ],
      }
    })
  }

  function handleRangeSelect(dates: string[]): void {
    setData([])
    setSearchParams((prev) => {
      const filters = _.remove(
        prev.filters,
        (filter) => filter.key != RANGE_FILTER_KEY
      )
      if (_.isEmpty(dates)) {
        return {
          ...initPagination,
          filters,
        }
      }
      return {
        ...initPagination,
        filters: [
          ...filters,
          {
            type: 'group',
            group: 'AND',
            key: RANGE_FILTER_KEY,
            conditions: [
              {
                type: 'isolated',
                property: 'created_at',
                operator: 'gte',
                value: dates[0],
              },
              {
                type: 'isolated',
                property: 'created_at',
                operator: 'lte',
                value: dates[1],
              },
            ],
          },
        ],
      }
    })
  }

  function handleStatusSelect(statuses: string[]): void {
    setData([])
    setSearchParams((prev) => {
      const filters = _.remove(
        prev.filters,
        (filter) => filter.key != STATUS_FILTER_KEY
      )
      if (_.isEmpty(statuses)) {
        return {
          ...initPagination,
          filters,
        }
      }
      return {
        ...initPagination,
        filters: _.concat(
          ...filters,
          statuses.map((value) => ({
            type: 'group',
            group: 'AND',
            key: STATUS_FILTER_KEY,
            conditions: [
              {
                type: 'isolated',
                property: 'status',
                operator: 'eq',
                value,
              },
            ],
          }))
        ),
      }
    })
  }

  function handleTextChange(text: string): void {
    setData([])
    setSearchParams((prev) => {
      const filters = _.remove(
        prev.filters,
        (filter) => filter.key != TEXT_FILTER_KEY
      )
      if (_.isEmpty(text)) {
        return {
          ...initPagination,
          filters,
          text: undefined,
        }
      }
      return {
        ...initPagination,
        filters,
        text,
        // TODO: recomment for detail search
        // filters: _.concat(...filters, [
        //   {
        //     type: 'group',
        //     group: 'AND',
        //     key: TEXT_FILTER_KEY,
        //     conditions: [
        //       {
        //         type: 'isolated',
        //         property: 'payload.data.values',
        //         operator: 'eq',
        //         value: text,
        //       },
        //     ],
        //   },
        // ]),
      }
    })
  }

  async function handleApproveObjects(
    ids: string[],
    reason?: string
  ): Promise<void> {
    setData([])
    try {
      await approve({
        approveDeclineShem: {
          objectsId: ids,
          reason,
        },
      }).unwrap()
      fetch({
        searchObject: searchParams,
      }).catch()
    } catch (error) {
      notification.error({
        message: 'Не удалось подтвердить объект',
      })
    }
  }

  async function handleDeclineObjects(
    ids: string[],
    reason?: string
  ): Promise<void> {
    setData([])
    try {
      await decline({
        approveDeclineShem: {
          objectsId: ids,
          reason,
        },
      }).unwrap()
      fetch({
        searchObject: searchParams,
      }).catch()
    } catch (error) {
      notification.error({
        message: 'Не удалось отклонить объект',
      })
    }
  }

  async function handleApproveByFilters(): Promise<void> {
    setData([])
    try {
      await approve({
        approveDeclineShem: {
          filters: searchParams.filters,
        },
      }).unwrap()
      fetch({
        searchObject: searchParams,
      }).catch()
    } catch (error) {
      notification.error({
        message: 'Не удалось подтвердить объекты',
      })
    }
  }

  async function handleDeclineByFilters(): Promise<void> {
    setData([])
    try {
      await decline({
        approveDeclineShem: {
          filters: searchParams.filters,
        },
      }).unwrap()
      fetch({
        searchObject: searchParams,
      }).catch()
    } catch (error) {
      notification.error({
        message: 'Не удалось отклонить объекты',
      })
    }
  }

  async function handleUploadFile(): Promise<void> {
    try {
      await downloadObjectFile({
        page: 1,
        count: Number.MAX_SAFE_INTEGER,
        filters: searchParams.filters,
      })
    } catch (error) {
      notification.error({
        description: 'Не удалось скачать файл',
        message: 'Ошибка',
      })
    }
  }

  async function handleUploadSelectedObjectsFile(
    objectIds: string[]
  ): Promise<void> {
    try {
      await downloadObjectFile({
        page: 1,
        count: Number.MAX_SAFE_INTEGER,
        filters: [
          {
            type: 'group',
            group: 'OR',
            conditions: objectIds.map((id) => ({
              type: 'isolated',
              property: '_id',
              operator: 'eq',
              value: id,
            })),
          },
        ],
      })
    } catch (error) {
      notification.error({
        description: 'Не удалось скачать файл',
        message: 'Ошибка',
      })
    }
  }

  return (
    <div>
      <Title level={2}>Загруженные объекты</Title>
      <Divider dashed></Divider>
      <ObjectListFiltersView
        onUserSelect={handleUserSelect}
        onModelSelect={handleModelSelect}
        onDatesSelect={handleRangeSelect}
        onStatusSelect={handleStatusSelect}
        onTextChange={debouncedText}
        approved={{
          onApprovedByFilter: handleApproveByFilters,
          onDeclinedByFilter: handleDeclineByFilters,
        }}
        isEmptyFilters={_.isEmpty(searchParams.filters)}
        downloaded={{
          onDwnloadFile: handleUploadFile,
        }}
      />
      <Divider dashed></Divider>
      <ObjectsListView
        data={data}
        isLoading={state.isLoading || totalState.isLoading}
        total={totalState.data?.total ?? 0}
        paginationParams={{
          page: searchParams.page ?? 0,
          count: searchParams.count ?? 0,
        }}
        setPagination={(value) => {
          setSearchParams((prev) => ({
            ...prev,
            ...value,
          }))
        }}
        onApproveObjects={(ids) => handleApproveObjects(ids)}
        onDeclineObjects={(ids) => handleDeclineObjects(ids)}
        onUploadObjectsFile={(ids) => handleUploadSelectedObjectsFile(ids)}
      />
    </div>
  )
}
