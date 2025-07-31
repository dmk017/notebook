import { GetProp, UploadProps } from 'antd'
import { Models, Payload2, Payload3 } from '../../store/main-api/generate/api'

export interface ModelPayloadType extends Payload2 {}

export interface ModelType extends Models {}

export interface AddObjectPayloadType extends Payload3 {}

export type FileType = Parameters<GetProp<UploadProps, 'beforeUpload'>>[0]
