import { UploadOutlined } from '@ant-design/icons'
import { Button, Upload, UploadFile } from 'antd'
import { UploadChangeParam, UploadProps } from 'antd/es/upload'
import { useState } from 'react'
import { useUploadFileApiV1FilesPostMutation } from '../../../store/main-api/generate/api'

interface UploadFormFieldProps {
  modelId: string
  onSuccesUpload: (fileId: string) => void
}

export function UploadFormField({
  modelId,
  onSuccesUpload,
}: UploadFormFieldProps): React.ReactElement {
  const [defaultFileList, setDefaultFileList] = useState<
    UploadChangeParam<UploadFile>['fileList']
  >([])

  const [uploadFile] = useUploadFileApiV1FilesPostMutation()

  const uploadImage: UploadProps['customRequest'] = async (options) => {
    const { file } = options
    try {
      const fd = new FormData()
      fd.append('file', file)
      const payload = await uploadFile({
        modelId: modelId,
        bodyUploadFileApiV1FilesPost: fd as unknown as {
          file: Blob
        },
      }).unwrap()
      options.onSuccess?.('Файл успешно загружен')
      onSuccesUpload(payload._id ?? '')
    } catch (err) {
      console.log('Eroor: ', err)
      const error = new Error('Ошибка загрузки файла')
      options.onError?.(error)
    }
  }

  const handleOnChange = (info: UploadChangeParam<UploadFile>) => {
    setDefaultFileList(info.fileList)
  }
  return (
    <Upload
      customRequest={uploadImage}
      onChange={handleOnChange}
      defaultFileList={defaultFileList}
    >
      <Button icon={<UploadOutlined />}>Нажмите для загрузки</Button>
    </Upload>
  )
}
