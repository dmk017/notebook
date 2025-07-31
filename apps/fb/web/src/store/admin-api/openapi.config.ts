import { ConfigFile } from '@rtk-query/codegen-openapi'

const config: ConfigFile = {
  schemaFile: `${
    process.env.ADMIN_API_URL ?? 'https://admin.4tuna.space'
  }/openapi.json`,
  apiFile: './empty.api.ts',
  outputFile: './generate/api.ts',
  apiImport: 'adminApiSlice',
  outputFiles: {
    './generate/api.ts': {
      filterEndpoints: [/.*/i],
    },
  },
  hooks: { queries: true, lazyQueries: true, mutations: true },
}

export default config
