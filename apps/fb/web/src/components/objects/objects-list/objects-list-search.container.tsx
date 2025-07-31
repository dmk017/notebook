import { useContext, useEffect, useState } from 'react'

import { Divider, notification, Typography } from 'antd'
import { useDebouncedCallback } from 'use-debounce'
import _ from 'lodash'
import { ObjectListFiltersView } from './objects-list-filters.view'
import { useObjectsSearchApiV1ObjectsSearchPostMutation } from '../../../store/main-api/generate/api'
import { ObjectType, SearchObjectWithKey } from '../objects.type'
import { ObjectsSearchResultView } from './objects-list-search.view'
import { downloadObjectFile } from '../../../store/file-download-file'
import { AuthUserContext } from '../../../providers/auth-user.provider'

const { Title } = Typography

const MODELS_FILTER_KEY = 'MODELS_FILTER'
const USERS_FILTER_KEY = 'USERS_FILTER'
const RANGE_FILTER_KEY = 'RANGE_FILTER'
const STATUS_FILTER_KEY = 'STATUS_FILTER'
const TEXT_FILTER_KEY = 'TEXT_FILTER'

export function ObjectsListSearch(): React.ReactElement {
  const { authUser } = useContext(AuthUserContext)
  const [data, setData] = useState<ObjectType[]>([])
  const debouncedText = useDebouncedCallback((value) => {
    handleTextChange(value)
  }, 500)
  const initPagination = {
    page: 1,
    count: 20,
  }
  const [searchParams, setSearchParams] = useState<SearchObjectWithKey>({
    ...initPagination,
    filters: [],
  })

  const [fetch, state] = useObjectsSearchApiV1ObjectsSearchPostMutation()

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

  return (
    <div>
      <Title level={2}>Поиск</Title>
      <Divider dashed></Divider>
      <ObjectListFiltersView
        onUserSelect={authUser?.role == 'USER' ? undefined : handleUserSelect}
        onModelSelect={handleModelSelect}
        onDatesSelect={handleRangeSelect}
        onStatusSelect={handleStatusSelect}
        onTextChange={debouncedText}
        isEmptyFilters={_.isEmpty(searchParams.filters)}
        downloaded={{
          onDwnloadFile: handleUploadFile,
        }}
      />
      <Divider dashed></Divider>
      <ObjectsSearchResultView
        data={data ?? []}
        isLoading={state.isLoading}
        hasMore={state.data?.is_next ?? true}
        nextFetch={() => {
          setSearchParams((prev) => ({
            ...prev,
            page: prev.page == null ? 1 : prev.page + 1,
          }))
        }}
      />
    </div>
  )
}
