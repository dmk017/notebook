import { mainApiSlice as api } from '../empty.api'
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    getPropertiesApiV1PropertiesListPost: build.mutation<
      GetPropertiesApiV1PropertiesListPostApiResponse,
      GetPropertiesApiV1PropertiesListPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/properties/list`,
        method: 'POST',
        body: queryArg.propertyListFilters,
        params: { page: queryArg.page, limit: queryArg.limit },
      }),
    }),
    addPropertyApiV1PropertiesPost: build.mutation<
      AddPropertyApiV1PropertiesPostApiResponse,
      AddPropertyApiV1PropertiesPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/properties/`,
        method: 'POST',
        body: queryArg.srcPropertiesPropertiesRouterApiSchemaPayload,
      }),
    }),
    getPropertyByIdApiV1PropertiesIdGet: build.query<
      GetPropertyByIdApiV1PropertiesIdGetApiResponse,
      GetPropertyByIdApiV1PropertiesIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/properties/${queryArg.id}` }),
    }),
    updatePropertyApiV1PropertiesIdPut: build.mutation<
      UpdatePropertyApiV1PropertiesIdPutApiResponse,
      UpdatePropertyApiV1PropertiesIdPutApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/properties/${queryArg.id}`,
        method: 'PUT',
        body: queryArg.srcPropertiesPropertiesRouterApiSchemaPayload,
      }),
    }),
    deletePropertyApiV1PropertiesIdDelete: build.mutation<
      DeletePropertyApiV1PropertiesIdDeleteApiResponse,
      DeletePropertyApiV1PropertiesIdDeleteApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/properties/${queryArg.id}`,
        method: 'DELETE',
      }),
    }),
    getPropertyHistoryApiV1PropertiesIdHistoryGet: build.query<
      GetPropertyHistoryApiV1PropertiesIdHistoryGetApiResponse,
      GetPropertyHistoryApiV1PropertiesIdHistoryGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/properties/${queryArg.id}/history`,
      }),
    }),
    recovePropertyApiV1PropertiesIdRecovePost: build.mutation<
      RecovePropertyApiV1PropertiesIdRecovePostApiResponse,
      RecovePropertyApiV1PropertiesIdRecovePostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/properties/${queryArg.id}/recove`,
        method: 'POST',
      }),
    }),
    getModelsApiV1ModelsListPost: build.mutation<
      GetModelsApiV1ModelsListPostApiResponse,
      GetModelsApiV1ModelsListPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/models/list`,
        method: 'POST',
        body: queryArg.modelsListFilter,
        params: { page: queryArg.page, limit: queryArg.limit },
      }),
    }),
    getModelByIdApiV1ModelsIdGet: build.query<
      GetModelByIdApiV1ModelsIdGetApiResponse,
      GetModelByIdApiV1ModelsIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/models/${queryArg.id}` }),
    }),
    updateModelApiV1ModelsIdPut: build.mutation<
      UpdateModelApiV1ModelsIdPutApiResponse,
      UpdateModelApiV1ModelsIdPutApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/models/${queryArg.id}`,
        method: 'PUT',
        body: queryArg.srcModelsModelsRouterApiSchemaPayload,
      }),
    }),
    deleteModelApiV1ModelsIdDelete: build.mutation<
      DeleteModelApiV1ModelsIdDeleteApiResponse,
      DeleteModelApiV1ModelsIdDeleteApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/models/${queryArg.id}`,
        method: 'DELETE',
      }),
    }),
    getModelHistoryApiV1ModelsIdHistoryGet: build.query<
      GetModelHistoryApiV1ModelsIdHistoryGetApiResponse,
      GetModelHistoryApiV1ModelsIdHistoryGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/models/${queryArg.id}/history` }),
    }),
    addModelApiV1ModelsPost: build.mutation<
      AddModelApiV1ModelsPostApiResponse,
      AddModelApiV1ModelsPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/models/`,
        method: 'POST',
        body: queryArg.srcModelsModelsRouterApiSchemaPayload,
      }),
    }),
    recoveModelApiV1ModelsIdRecovePost: build.mutation<
      RecoveModelApiV1ModelsIdRecovePostApiResponse,
      RecoveModelApiV1ModelsIdRecovePostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/models/${queryArg.id}/recove`,
        method: 'POST',
      }),
    }),
    getExampleFileModedlApiV1ModelsIdExampleFileGet: build.query<
      GetExampleFileModedlApiV1ModelsIdExampleFileGetApiResponse,
      GetExampleFileModedlApiV1ModelsIdExampleFileGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/models/${queryArg.id}/example/file`,
      }),
    }),
    getAllObjectsApiV1ObjectsGet: build.query<
      GetAllObjectsApiV1ObjectsGetApiResponse,
      GetAllObjectsApiV1ObjectsGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/objects/`,
        params: { page: queryArg.page, limit: queryArg.limit },
      }),
    }),
    addObjectApiV1ObjectsPost: build.mutation<
      AddObjectApiV1ObjectsPostApiResponse,
      AddObjectApiV1ObjectsPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/objects/`,
        method: 'POST',
        body: queryArg.srcObjectsObjectsRouterApiSchemaPayload,
      }),
    }),
    getCountObjectsApiV1ObjectsCountGet: build.query<
      GetCountObjectsApiV1ObjectsCountGetApiResponse,
      GetCountObjectsApiV1ObjectsCountGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/objects/count`,
        params: { page: queryArg.page, limit: queryArg.limit },
      }),
    }),
    getObjectApiV1ObjectsIdGet: build.query<
      GetObjectApiV1ObjectsIdGetApiResponse,
      GetObjectApiV1ObjectsIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/objects/${queryArg.id}` }),
    }),
    uploadFileApiV1ObjectsPackageFilePost: build.mutation<
      UploadFileApiV1ObjectsPackageFilePostApiResponse,
      UploadFileApiV1ObjectsPackageFilePostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/objects/package/file`,
        method: 'POST',
        body: queryArg.bodyUploadFileApiV1ObjectsPackageFilePost,
      }),
    }),
    objectsSearchApiV1ObjectsSearchPost: build.mutation<
      ObjectsSearchApiV1ObjectsSearchPostApiResponse,
      ObjectsSearchApiV1ObjectsSearchPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/objects/search`,
        method: 'POST',
        body: queryArg.searchObject,
      }),
    }),
    declineObjectsApiV1ObjectsDeclinePut: build.mutation<
      DeclineObjectsApiV1ObjectsDeclinePutApiResponse,
      DeclineObjectsApiV1ObjectsDeclinePutApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/objects/decline`,
        method: 'PUT',
        body: queryArg.approveDeclineShem,
      }),
    }),
    approveObjectsApiV1ObjectsApprovePut: build.mutation<
      ApproveObjectsApiV1ObjectsApprovePutApiResponse,
      ApproveObjectsApiV1ObjectsApprovePutApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/objects/approve`,
        method: 'PUT',
        body: queryArg.approveDeclineShem,
      }),
    }),
    unloadingObgectsApiV1ObjectsUnloadingPost: build.mutation<
      UnloadingObgectsApiV1ObjectsUnloadingPostApiResponse,
      UnloadingObgectsApiV1ObjectsUnloadingPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/objects/unloading`,
        method: 'POST',
        body: queryArg.searchObject,
      }),
    }),
    uploadFileApiV1FilesPost: build.mutation<
      UploadFileApiV1FilesPostApiResponse,
      UploadFileApiV1FilesPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/files/`,
        method: 'POST',
        body: queryArg.bodyUploadFileApiV1FilesPost,
        params: { model_id: queryArg.modelId },
      }),
    }),
    downloadFileApiV1FilesFileIdGet: build.query<
      DownloadFileApiV1FilesFileIdGetApiResponse,
      DownloadFileApiV1FilesFileIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/files/${queryArg.fileId}` }),
    }),
    getMeApiV1AuthMeGet: build.query<
      GetMeApiV1AuthMeGetApiResponse,
      GetMeApiV1AuthMeGetApiArg
    >({
      query: () => ({ url: `/api/v1/auth/me` }),
    }),
    getTokenApiV1AuthTokenGet: build.query<
      GetTokenApiV1AuthTokenGetApiResponse,
      GetTokenApiV1AuthTokenGetApiArg
    >({
      query: () => ({ url: `/api/v1/auth/token` }),
    }),
    getUserApiV1AuthUserIdGet: build.query<
      GetUserApiV1AuthUserIdGetApiResponse,
      GetUserApiV1AuthUserIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/auth/${queryArg.userId}` }),
    }),
    updateAccessModelsApiV1AuthModelsPut: build.mutation<
      UpdateAccessModelsApiV1AuthModelsPutApiResponse,
      UpdateAccessModelsApiV1AuthModelsPutApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/auth/models`,
        method: 'PUT',
        body: queryArg.accessModelNames,
        params: { user_id: queryArg.userId },
      }),
    }),
  }),
  overrideExisting: false,
})
export { injectedRtkApi as enhancedApi }
export type GetPropertiesApiV1PropertiesListPostApiResponse =
  /** status 200 Successful Response */ Properties[]
export type GetPropertiesApiV1PropertiesListPostApiArg = {
  page?: number
  limit?: number
  propertyListFilters: PropertyListFilters
}
export type AddPropertyApiV1PropertiesPostApiResponse =
  /** status 200 Successful Response */ Properties
export type AddPropertyApiV1PropertiesPostApiArg = {
  srcPropertiesPropertiesRouterApiSchemaPayload: Payload
}
export type GetPropertyByIdApiV1PropertiesIdGetApiResponse =
  /** status 200 Successful Response */ Properties | null
export type GetPropertyByIdApiV1PropertiesIdGetApiArg = {
  id: string
}
export type UpdatePropertyApiV1PropertiesIdPutApiResponse =
  /** status 200 Successful Response */ Properties
export type UpdatePropertyApiV1PropertiesIdPutApiArg = {
  id: string
  srcPropertiesPropertiesRouterApiSchemaPayload: Payload
}
export type DeletePropertyApiV1PropertiesIdDeleteApiResponse =
  /** status 200 Successful Response */ Properties
export type DeletePropertyApiV1PropertiesIdDeleteApiArg = {
  id: string
}
export type GetPropertyHistoryApiV1PropertiesIdHistoryGetApiResponse =
  /** status 200 Successful Response */ Properties[]
export type GetPropertyHistoryApiV1PropertiesIdHistoryGetApiArg = {
  id: string
}
export type RecovePropertyApiV1PropertiesIdRecovePostApiResponse =
  /** status 200 Successful Response */ Properties
export type RecovePropertyApiV1PropertiesIdRecovePostApiArg = {
  id: string
}
export type GetModelsApiV1ModelsListPostApiResponse =
  /** status 200 Successful Response */ ListResponse
export type GetModelsApiV1ModelsListPostApiArg = {
  page?: number
  limit?: number
  modelsListFilter: ModelsListFilter
}
export type GetModelByIdApiV1ModelsIdGetApiResponse =
  /** status 200 Successful Response */ Models | null
export type GetModelByIdApiV1ModelsIdGetApiArg = {
  id: string
}
export type UpdateModelApiV1ModelsIdPutApiResponse =
  /** status 200 Successful Response */ Models2
export type UpdateModelApiV1ModelsIdPutApiArg = {
  id: string
  srcModelsModelsRouterApiSchemaPayload: Payload2
}
export type DeleteModelApiV1ModelsIdDeleteApiResponse =
  /** status 200 Successful Response */ Models2
export type DeleteModelApiV1ModelsIdDeleteApiArg = {
  id: string
}
export type GetModelHistoryApiV1ModelsIdHistoryGetApiResponse =
  /** status 200 Successful Response */ Models[]
export type GetModelHistoryApiV1ModelsIdHistoryGetApiArg = {
  id: string
}
export type AddModelApiV1ModelsPostApiResponse =
  /** status 200 Successful Response */ Models2
export type AddModelApiV1ModelsPostApiArg = {
  srcModelsModelsRouterApiSchemaPayload: Payload2
}
export type RecoveModelApiV1ModelsIdRecovePostApiResponse =
  /** status 200 Successful Response */ Models2
export type RecoveModelApiV1ModelsIdRecovePostApiArg = {
  id: string
}
export type GetExampleFileModedlApiV1ModelsIdExampleFileGetApiResponse =
  /** status 200 Successful Response */ void
export type GetExampleFileModedlApiV1ModelsIdExampleFileGetApiArg = {
  id: string
}
export type GetAllObjectsApiV1ObjectsGetApiResponse =
  /** status 200 Successful Response */ ListResponse
export type GetAllObjectsApiV1ObjectsGetApiArg = {
  page?: number
  limit?: number
}
export type AddObjectApiV1ObjectsPostApiResponse =
  /** status 200 Successful Response */ Objects
export type AddObjectApiV1ObjectsPostApiArg = {
  srcObjectsObjectsRouterApiSchemaPayload: Payload3
}
export type GetCountObjectsApiV1ObjectsCountGetApiResponse =
  /** status 200 Successful Response */ CountObjectsResposnse
export type GetCountObjectsApiV1ObjectsCountGetApiArg = {
  page?: number
  limit?: number
}
export type GetObjectApiV1ObjectsIdGetApiResponse =
  /** status 200 Successful Response */ Objects | null
export type GetObjectApiV1ObjectsIdGetApiArg = {
  id: string
}
export type UploadFileApiV1ObjectsPackageFilePostApiResponse =
  /** status 200 Successful Response */ TResponseObject
export type UploadFileApiV1ObjectsPackageFilePostApiArg = {
  bodyUploadFileApiV1ObjectsPackageFilePost: BodyUploadFileApiV1ObjectsPackageFilePost
}
export type ObjectsSearchApiV1ObjectsSearchPostApiResponse =
  /** status 200 Successful Response */ ListResponse
export type ObjectsSearchApiV1ObjectsSearchPostApiArg = {
  searchObject: SearchObject
}
export type DeclineObjectsApiV1ObjectsDeclinePutApiResponse =
  /** status 200 Successful Response */ number
export type DeclineObjectsApiV1ObjectsDeclinePutApiArg = {
  approveDeclineShem: ApproveDeclineShem
}
export type ApproveObjectsApiV1ObjectsApprovePutApiResponse =
  /** status 200 Successful Response */ number
export type ApproveObjectsApiV1ObjectsApprovePutApiArg = {
  approveDeclineShem: ApproveDeclineShem
}
export type UnloadingObgectsApiV1ObjectsUnloadingPostApiResponse =
  /** status 200 Successful Response */ void
export type UnloadingObgectsApiV1ObjectsUnloadingPostApiArg = {
  searchObject: SearchObject
}
export type UploadFileApiV1FilesPostApiResponse =
  /** status 200 Successful Response */ Files
export type UploadFileApiV1FilesPostApiArg = {
  modelId: string
  bodyUploadFileApiV1FilesPost: BodyUploadFileApiV1FilesPost
}
export type DownloadFileApiV1FilesFileIdGetApiResponse =
  /** status 200 Successful Response */ any
export type DownloadFileApiV1FilesFileIdGetApiArg = {
  fileId: string
}
export type GetMeApiV1AuthMeGetApiResponse =
  /** status 200 Successful Response */ User
export type GetMeApiV1AuthMeGetApiArg = void
export type GetTokenApiV1AuthTokenGetApiResponse =
  /** status 200 Successful Response */ UserTokenResponse
export type GetTokenApiV1AuthTokenGetApiArg = void
export type GetUserApiV1AuthUserIdGetApiResponse =
  /** status 200 Successful Response */ Auth | null
export type GetUserApiV1AuthUserIdGetApiArg = {
  userId: string
}
export type UpdateAccessModelsApiV1AuthModelsPutApiResponse =
  /** status 200 Successful Response */ Auth | null
export type UpdateAccessModelsApiV1AuthModelsPutApiArg = {
  userId: string
  accessModelNames: string[]
}
export type PrimitiveTypeEnum = 'STR' | 'NUMBER' | 'DATE' | 'BOOL' | 'FILE'
export type PropertyPayload = {
  name: string
  primitive_type: PrimitiveTypeEnum
  help_text?: string | null
  is_required?: boolean
  is_multiple?: boolean
  validation?: string
}
export type Properties = {
  _id?: string
  name: string
  owner_id: string
  created_at?: any
  properties: PropertyPayload[]
  next_id: string | null
  deleted?: boolean
}
export type ValidationError = {
  loc: (string | number)[]
  msg: string
  type: string
}
export type HttpValidationError = {
  detail?: ValidationError[]
}
export type PropertyListFilters = {
  name?: string | null
  is_deleted?: boolean | null
}
export type Payload = {
  name: string
  properties: PropertyPayload[]
}
export type ListResponse = {
  count: number
  page_number: number
  is_next: boolean
  data: any[]
}
export type ModelsListFilter = {
  name?: string | null
  is_deleted?: boolean | null
  is_actual?: boolean | null
}
export type ResponsePropertyPayload = {
  payload: Properties
  is_required: boolean
}
export type Models = {
  _id?: string
  name: string
  owner_id: string
  created_at?: any
  properties: ResponsePropertyPayload[]
  next_id: string | null
  deleted?: boolean
}
export type ModelPropertyPayload = {
  id: string
  is_required?: boolean
}
export type Models2 = {
  _id?: string
  name: string
  owner_id: string
  created_at?: any
  properties: ModelPropertyPayload[]
  next_id: string | null
  deleted?: boolean
}
export type PropertiesPayload = {
  id: string
  is_required: boolean
}
export type Payload2 = {
  name: string
  properties: PropertiesPayload[]
}
export type ObjectStatus = {
  approve_at?: string | null
  decline_at?: string | null
  reason?: string | null
  moderator_id?: string | null
}
export type TPayloadData = {
  name: string
  values: any[]
  type: any
}
export type ObjectPropertyPayload = {
  property_name: string
  data: TPayloadData[]
}
export type Objects = {
  _id?: string
  created_at?: any
  status?: ObjectStatus
  owner_id: string
  model_id: string
  deleted?: boolean
  payload: ObjectPropertyPayload[]
}
export type TPayloadValues = {
  name: string
  values: any[]
}
export type PropertyPayloadValues = {
  property_name: string
  data: TPayloadValues[]
}
export type Payload3 = {
  model_id: string
  properties: PropertyPayloadValues[]
}
export type CountObjectsResposnse = {
  total: number
}
export type Object = {
  id: string
  created_at: string
  status: ObjectStatus
  owner_id: string
  model_id: string
  payload?: PropertyPayloadValues[] | null
}
export type ErrorModel = {
  message: string
  code: number
}
export type ReponseError = {
  code: ErrorModel
  details?: string
}
export type TResponseObject = {
  success: boolean
  message?: string
  data?: Object | null
  errors?: ReponseError[]
}
export type BodyUploadFileApiV1ObjectsPackageFilePost = {
  file: Blob
}
export type SearchFilter = {
  type: 'isolated'
  /** Характеристика */
  property: string
  /** Оператор для запроса */
  operator: string
  value: any
}
export type SearchFiltersList = {
  type: 'group'
  group?: ('OR' | 'AND') | null
  conditions: (SearchFilter | SearchFiltersList)[]
}
export type SearchObject = {
  text?: string
  page?: number
  count?: number
  filters: SearchFiltersList[]
}
export type ApproveDeclineShem = {
  objectsId?: string[] | null
  filters?: SearchFiltersList[] | null
  reason?: string | null
}
export type Files = {
  _id?: string
  model_id: string
  owner_id: string
  path: string
  original_name: string
  extension: string
  type: string
  created_at?: any
}
export type BodyUploadFileApiV1FilesPost = {
  file: Blob
}
export type UserRole = 'ADMIN' | 'MODERATOR' | 'USER'
export type User = {
  user_id: string
  user_name: string
  role: UserRole
}
export type UserTokenResponse = {
  token: string
}
export type Auth = {
  _id?: string
  user_id: string
  user_name: string
  access_model_names?: string[]
}
export const {
  useGetPropertiesApiV1PropertiesListPostMutation,
  useAddPropertyApiV1PropertiesPostMutation,
  useGetPropertyByIdApiV1PropertiesIdGetQuery,
  useLazyGetPropertyByIdApiV1PropertiesIdGetQuery,
  useUpdatePropertyApiV1PropertiesIdPutMutation,
  useDeletePropertyApiV1PropertiesIdDeleteMutation,
  useGetPropertyHistoryApiV1PropertiesIdHistoryGetQuery,
  useLazyGetPropertyHistoryApiV1PropertiesIdHistoryGetQuery,
  useRecovePropertyApiV1PropertiesIdRecovePostMutation,
  useGetModelsApiV1ModelsListPostMutation,
  useGetModelByIdApiV1ModelsIdGetQuery,
  useLazyGetModelByIdApiV1ModelsIdGetQuery,
  useUpdateModelApiV1ModelsIdPutMutation,
  useDeleteModelApiV1ModelsIdDeleteMutation,
  useGetModelHistoryApiV1ModelsIdHistoryGetQuery,
  useLazyGetModelHistoryApiV1ModelsIdHistoryGetQuery,
  useAddModelApiV1ModelsPostMutation,
  useRecoveModelApiV1ModelsIdRecovePostMutation,
  useGetExampleFileModedlApiV1ModelsIdExampleFileGetQuery,
  useLazyGetExampleFileModedlApiV1ModelsIdExampleFileGetQuery,
  useGetAllObjectsApiV1ObjectsGetQuery,
  useLazyGetAllObjectsApiV1ObjectsGetQuery,
  useAddObjectApiV1ObjectsPostMutation,
  useGetCountObjectsApiV1ObjectsCountGetQuery,
  useLazyGetCountObjectsApiV1ObjectsCountGetQuery,
  useGetObjectApiV1ObjectsIdGetQuery,
  useLazyGetObjectApiV1ObjectsIdGetQuery,
  useUploadFileApiV1ObjectsPackageFilePostMutation,
  useObjectsSearchApiV1ObjectsSearchPostMutation,
  useDeclineObjectsApiV1ObjectsDeclinePutMutation,
  useApproveObjectsApiV1ObjectsApprovePutMutation,
  useUnloadingObgectsApiV1ObjectsUnloadingPostMutation,
  useUploadFileApiV1FilesPostMutation,
  useDownloadFileApiV1FilesFileIdGetQuery,
  useLazyDownloadFileApiV1FilesFileIdGetQuery,
  useGetMeApiV1AuthMeGetQuery,
  useLazyGetMeApiV1AuthMeGetQuery,
  useGetTokenApiV1AuthTokenGetQuery,
  useLazyGetTokenApiV1AuthTokenGetQuery,
  useGetUserApiV1AuthUserIdGetQuery,
  useLazyGetUserApiV1AuthUserIdGetQuery,
  useUpdateAccessModelsApiV1AuthModelsPutMutation,
} = injectedRtkApi
