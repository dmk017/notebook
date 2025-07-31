import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const API_URL = `${process.env.ADMIN_API_URL}`

async function getAccessToken(): Promise<string> {
  const response = await fetch(`${process.env.BACKEND_URL}/api/v1/auth/token`)
  if (!response.ok) {
    throw Error(`Error fetch token: ${await response.text()}`)
  }
  const data = await response.json()
  return data['token']
}

export const adminApiSlice = createApi({
  reducerPath: 'adminApi',
  baseQuery: fetchBaseQuery({
    baseUrl: API_URL,
    prepareHeaders: async (headers) => {
      const accessToken = await getAccessToken()
      headers.set('Authorization', `Bearer ${accessToken}`)
      return headers
    },
  }),
  endpoints: () => ({}),
})
