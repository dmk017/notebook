import { ConfigFile } from '@rtk-query/codegen-openapi'

const config: ConfigFile = {
  schemaFile: `${
    process.env.BACKEND_URL ?? 'http://127.0.0.1:5002'
  }/openapi.json`,
  apiFile: './empty.api.ts',
  outputFile: './generate/api.ts',
  apiImport: 'mainApiSlice',
  outputFiles: {
    './generate/api.ts': {
      filterEndpoints: [/.*/i],
    },
  },
  hooks: { queries: true, lazyQueries: true, mutations: true },
}

export default config
