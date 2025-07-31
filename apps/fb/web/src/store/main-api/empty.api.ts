import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import Cookies from 'js-cookie'

const API_URL = `${process.env.BACKEND_URL}`

export const mainApiSlice = createApi({
  reducerPath: 'mainApi',
  baseQuery: fetchBaseQuery({
    baseUrl: API_URL,
    prepareHeaders: (headers) => {
      const cookies = Cookies.get()
      const cookesString = Object.entries(cookies)
        .map((pair) => pair.join('='))
        .join(';')
      headers.set('Cookie', cookesString)

      return headers
    },
  }),
  endpoints: () => ({}),
})
