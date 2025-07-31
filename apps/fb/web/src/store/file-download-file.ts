// import Path from 'path'

const API_URL = `${process.env.BACKEND_URL}`

async function downloadFile(
  path: string,
  method: 'GET' | 'POST',
  headers?: Record<string, string>,
  body?: string
) {
  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body,
  })
  if (!response.ok) {
    throw new Error(await response.text())
  }
  const blob = await response.blob()

  const url = window.URL.createObjectURL(blob)
  const tempLink = document.createElement('a')
  tempLink.href = url
  // const contentDesposition =
  //   response.headers.get('content-disposition')?.split('"')[1] ?? 'temp.xls'
  // const filename = Path.parse(contentDesposition).name
  // tempLink.setAttribute('download', `${filename}.xls`)

  document.body.appendChild(tempLink)
  tempLink.click()

  document.body.removeChild(tempLink)
  window.URL.revokeObjectURL(url)
}

export async function downloadObjectFile(filters: object): Promise<void> {
  const headers = { 'Content-Type': 'application/json' }
  try {
    await downloadFile(
      '/api/v1/objects/unloading',
      'POST',
      headers,
      JSON.stringify(filters)
    )
  } catch (error) {
    throw new Error(`Error: ${error}`)
  }
}

export async function downloadExampleModelFile(modelId: string): Promise<void> {
  try {
    await downloadFile(`/api/v1/models/${modelId}/example/file`, 'GET')
  } catch (error) {
    throw new Error(`Error: ${error}`)
  }
}
