type Result<T> = { data: T, error: null } | { data: null, error: Error };
type DeleteDataResult = { data: {success: true}, error: null } | { data: null, error: Error };
type typeDownloadDataResult = { data: {success: true}, error: null } | {data: null, error: Error }

export async function useApi<T>(request: RequestInfo): Promise<Result<T>> {
  try {
    const response = await fetch(request);
    if (!response.ok) {
      const error = new Error(`${response.status} ${response.statusText}`);
      return { data: null, error };
    }
    const data: T = await response.json();
    return { data, error: null };
  }
  catch (error) {
      return { data: null, error: error as Error };
    }
}


export async function deleteDataUseApi(request: RequestInfo): Promise<DeleteDataResult> {
  try {
    const response = await fetch(request);
    if (!response.ok) {
      const error = new Error(`${response.status} ${response.statusText}`);
      return { data: null, error };
    }
    return { data: {success: true}, error: null };
  }
  catch (error) {
    console.log(error);
      return { data: null, error: error as Error };
    }
}


export async function downloadFileUseApi(request: RequestInfo): Promise<typeDownloadDataResult> {
  try {
    const response = await fetch(request);
    if (!response.ok) {
      const error = new Error(`${response.status} ${response.statusText}`);
      return { data: null, error };
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', "client.ovpn");
    document.body.appendChild(link);
    link.click();
    link.parentNode?.removeChild(link);
    window.URL.revokeObjectURL(url);
    return { data: {success: true}, error: null };
  }
  catch (error) {
    console.log(error);
      return { data: null, error: error as Error };
    }
}

