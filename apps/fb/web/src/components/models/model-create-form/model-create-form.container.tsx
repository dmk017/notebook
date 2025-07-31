import { notification, Spin } from 'antd'
import { useAsyncFn } from 'react-use'
import {
  PropertyPayloadValues,
  ReponseError,
  useAddObjectApiV1ObjectsPostMutation,
  useGetModelByIdApiV1ModelsIdGetQuery,
} from '../../../store/main-api/generate/api'
import { ModelCreateFromView } from './model-create-form.view'
import { AddObjectPayloadType, FileType } from '../models.type'
import router from 'next/router'
import { RootRoutingPath } from '../../../routes'
import _ from 'lodash'
import { downloadExampleModelFile } from '../../../store/file-download-file'
import { uploadObjectsFile } from '../../../store/file-upload-api'
import { useState } from 'react'

interface ModelCreateFromProps {
  modelId: string
}

export function ModelCreateFrom({
  modelId,
}: ModelCreateFromProps): React.ReactElement {
  const [errors, setErrors] = useState<ReponseError[]>([])
  const state = useGetModelByIdApiV1ModelsIdGetQuery({
    id: modelId,
  })

  const [addObject] = useAddObjectApiV1ObjectsPostMutation()
  const [uploadFileState, uploadFile] = useAsyncFn(
    async (file: FileType) => {
      const response = await uploadObjectsFile(file)
      return response
    },
    [uploadObjectsFile]
  )
  const [downloadExampleFileState, downloadExampleFile] = useAsyncFn(
    async () => {
      try {
        await downloadExampleModelFile(modelId)
      } catch (error) {
        notification.error({
          message: 'Ошибка',
          description: JSON.stringify(error),
        })
      }
    }
  )

  async function handleClickCreateObject(
    data: AddObjectPayloadType['properties']
  ): Promise<void> {
    try {
      const properties: PropertyPayloadValues[] = Object.entries(data)
        .map(([key, value]) => {
          const [propertyName, primitiveName] = _.split(key, '-', 2)
          return {
            property_name: propertyName,
            data: {
              name: primitiveName,
              value,
            },
          }
        })
        .reduce((prev, cur) => {
          const propertyName = cur.property_name
          const propertyIndex = _.findIndex(
            prev,
            (o) => o.property_name == cur.property_name
          )

          const primitiveValue =
            cur.data.value instanceof Array ? cur.data.value : [cur.data.value]

          // если такой проперти не встретилось
          if (propertyIndex == -1) {
            prev.push({
              property_name: propertyName,
              data: [
                {
                  name: cur.data.name,
                  values: primitiveValue,
                },
              ],
            })
            return prev
          }

          // если проперть есть, смотрим примитивное поле
          const primitiveIndex = _.findIndex(
            prev[propertyIndex].data,
            (o) => o.name == cur.data.name
          )

          // если такого примитивного поля нет - добавляем
          if (primitiveIndex == -1) {
            prev[propertyIndex].data.push({
              name: cur.data.name,
              values: primitiveValue,
            })
            return prev
          }

          prev[propertyIndex].data[primitiveIndex].values = _.concat(
            prev[propertyIndex].data[primitiveIndex].values,
            primitiveValue
          )

          return prev
        }, [] as PropertyPayloadValues[])
      await addObject({
        srcObjectsObjectsRouterApiSchemaPayload: {
          model_id: modelId,
          properties,
        },
      }).unwrap()
      notification.success({
        message: 'Успех',
        description: 'Модель успешно добавлена',
        onClose: () => {
          router.push(RootRoutingPath.MODELS, undefined, {
            shallow: true,
          })
        },
        showProgress: true,
        pauseOnHover: false,
      })
    } catch (error) {
      notification.error({
        message: 'Ошибка',
      })
    }
  }

  async function handleUploadObjectsFile(file: FileType) {
    setErrors([])
    try {
      const response = await uploadFile(file)
      if (response.errors != null && response.errors.length > 0) {
        notification.warning({
          message: 'Ошибка',
          description: 'Ошибка при парсинге',
        })
        setErrors(response.errors)
        return
      }
      notification.success({
        message: 'Успех',
        description: response.message,
        onClose: () => {
          router.push(RootRoutingPath.MODELS, undefined, {
            shallow: true,
          })
        },
        showProgress: true,
        pauseOnHover: false,
      })
    } catch (error) {
      notification.error({
        message: 'Ошибка',
      })
    }
  }

  if (state.isLoading || state.data == null) {
    return <Spin />
  }

  return (
    <ModelCreateFromView
      model={state.data}
      parseErrors={errors}
      onSubmit={handleClickCreateObject}
      onClickDownlodExampleFileLink={downloadExampleFile}
      isLoadingDownloadFile={downloadExampleFileState.loading}
      onSubmitFileUpload={handleUploadObjectsFile}
      isLoadingUploadFile={uploadFileState.loading}
    />
  )
}
