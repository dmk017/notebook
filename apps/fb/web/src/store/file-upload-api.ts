import { FileType } from '../components/models/models.type'
import { TResponseObject } from './main-api/generate/api'

const API_URL = `${process.env.BACKEND_URL}`

export async function uploadFile(
  path: string,
  method: 'GET' | 'POST',
  headers?: Record<string, string>,
  body?: FormData
): Promise<Response> {
  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body,
  })

  if (!response.ok) {
    throw new Error(await response.text())
  }
  return response
}

export async function uploadObjectsFile(file: Blob): Promise<TResponseObject> {
  const data = new FormData()
  data.append('file', file as FileType)
  try {
    const response = await uploadFile(
      '/api/v1/objects/package/file',
      'POST',
      {
        contentType: 'multipart/form-data',
      },
      data
    )
    return response.json()
  } catch (error) {
    throw new Error(`Error: ${error}`)
  }
}
