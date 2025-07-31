import { adminApiSlice as api } from '../empty.api'
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    getUserByIdApiV1UsersUserIdGet: build.query<
      GetUserByIdApiV1UsersUserIdGetApiResponse,
      GetUserByIdApiV1UsersUserIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/users/${queryArg.userId}` }),
    }),
    getUserGroupsApiV1UsersUserIdGroupsGet: build.query<
      GetUserGroupsApiV1UsersUserIdGroupsGetApiResponse,
      GetUserGroupsApiV1UsersUserIdGroupsGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/users/${queryArg.userId}/groups` }),
    }),
    getGroupByIdApiV1GroupsGroupIdGet: build.query<
      GetGroupByIdApiV1GroupsGroupIdGetApiResponse,
      GetGroupByIdApiV1GroupsGroupIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/groups/${queryArg.groupId}` }),
    }),
    getGroupByIdApiV1GroupsGroupIdMembersGet: build.query<
      GetGroupByIdApiV1GroupsGroupIdMembersGetApiResponse,
      GetGroupByIdApiV1GroupsGroupIdMembersGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/groups/${queryArg.groupId}/members`,
      }),
    }),
    getGroupByIdApiV1GroupsGroupIdAllGet: build.query<
      GetGroupByIdApiV1GroupsGroupIdAllGetApiResponse,
      GetGroupByIdApiV1GroupsGroupIdAllGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/groups/${queryArg.groupId}/all` }),
    }),
  }),
  overrideExisting: false,
})
export { injectedRtkApi as enhancedApi }
export type GetUserByIdApiV1UsersUserIdGetApiResponse =
  /** status 200 Successful Response */ UserData | null
export type GetUserByIdApiV1UsersUserIdGetApiArg = {
  userId: string
}
export type GetUserGroupsApiV1UsersUserIdGroupsGetApiResponse =
  /** status 200 Successful Response */ GroupData[]
export type GetUserGroupsApiV1UsersUserIdGroupsGetApiArg = {
  userId: string
}
export type GetGroupByIdApiV1GroupsGroupIdGetApiResponse =
  /** status 200 Successful Response */ GroupData
export type GetGroupByIdApiV1GroupsGroupIdGetApiArg = {
  groupId: string
}
export type GetGroupByIdApiV1GroupsGroupIdMembersGetApiResponse =
  /** status 200 Successful Response */ UserData[]
export type GetGroupByIdApiV1GroupsGroupIdMembersGetApiArg = {
  groupId: string
}
export type GetGroupByIdApiV1GroupsGroupIdAllGetApiResponse =
  /** status 200 Successful Response */ UserData[]
export type GetGroupByIdApiV1GroupsGroupIdAllGetApiArg = {
  groupId: string
}
export type UserData = {
  id: string
  username: string
  firstName: string
  lastName: string
  email: string
}
export type ValidationError = {
  loc: (string | number)[]
  msg: string
  type: string
}
export type HttpValidationError = {
  detail?: ValidationError[]
}
export type GroupData = {
  id: string
  name: string
  path: string
  parentId?: string | null
  subGroups: GroupData[]
}
export const {
  useGetUserByIdApiV1UsersUserIdGetQuery,
  useLazyGetUserByIdApiV1UsersUserIdGetQuery,
  useGetUserGroupsApiV1UsersUserIdGroupsGetQuery,
  useLazyGetUserGroupsApiV1UsersUserIdGroupsGetQuery,
  useGetGroupByIdApiV1GroupsGroupIdGetQuery,
  useLazyGetGroupByIdApiV1GroupsGroupIdGetQuery,
  useGetGroupByIdApiV1GroupsGroupIdMembersGetQuery,
  useLazyGetGroupByIdApiV1GroupsGroupIdMembersGetQuery,
  useGetGroupByIdApiV1GroupsGroupIdAllGetQuery,
  useLazyGetGroupByIdApiV1GroupsGroupIdAllGetQuery,
} = injectedRtkApi
