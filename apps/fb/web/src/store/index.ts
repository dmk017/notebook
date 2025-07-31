import { configureStore } from '@reduxjs/toolkit'
import { adminApiSlice } from './admin-api/empty.api'
import { mainApiSlice } from './main-api/empty.api'

export const store = configureStore({
  reducer: {
    [adminApiSlice.reducerPath]: adminApiSlice.reducer,
    [mainApiSlice.reducerPath]: mainApiSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      adminApiSlice.middleware,
      mainApiSlice.middleware
    ),
})
