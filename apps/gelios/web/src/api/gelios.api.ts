import { deleteDataUseApi, downloadFileUseApi, useApi } from "@/hooks";
import { ServerStates } from "@/components/servers/serversStates";
import { 
  ServerListResponse, 
  ServerBaseResponse, 
  GroupUsers, 
  ChainResponse, 
  ChainListResponse, 
  ChainClientResponse,
  User
} from "./gelios.types";
import { ChainStates } from "@/components/chains/chainsStates";

// TODO: разобраться с headers

export async function GetServers(
    data: {
      server_status: ServerStates | null,
      owner_id: string | null,
      count: number,
      page_number: number
    }
) {
  return await useApi<ServerListResponse>(
    new Request(
    `${process.env.BACKEND_URL}/api/v1/servers/list`,
    {
      method: "post",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
      },
    )
  )
};



export async function DeleteServer(
  serverId: number
) {
  return await deleteDataUseApi(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/servers/${serverId}`,
      {
        method: "delete",
      }
    )
  )
}


export async function AddServer(
  data: {
    created_data: {
      name: string,
      login: string,
      password: string,
      ip: string,
      country: string
    }
  }
) {
  return await useApi<ServerBaseResponse>(
    new Request(
    `${process.env.BACKEND_URL}/api/v1/servers`,
    {
      method: "post",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
      },
    )
  )
}


export async function GetServer(serverId: string) {
  return await useApi<ServerBaseResponse>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/servers/${serverId}`,
      {
        method: "get",
        headers: {
          'Content-Type': 'application/json',
        },
      },
    )
  )
}


export async function ChangeServer(
  data: {
    updated_data: {
      name: string,
      login: string,
      password: string,
      ip: string,
      country: string
    },
    server_id: string
}) {
  return await useApi<ServerBaseResponse>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/servers/change`,
      {
        method: "put",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      },
    )
  )
}


export async function GetGeliosUsers() {
  const data = await useApi<GroupUsers>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/users/list`,
      {
        method: "get",
        headers: {
          'Content-Type': 'application/json',
        },
      },
    )
  )
  return data
}


export async function UpdateServerOwner(
  data: {
    owner_id: string,
    server_id: number
  }
) {
  return await useApi<ServerBaseResponse>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/servers/update_owner`,
      {
        method: "put",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      },
    )
  )
}

export async function AddChain(
  data: {
    name: string,
    servers_ids: number[]
}) {
  return await useApi<ChainResponse>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/chains`,
      {
        method: "post",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      },
    )
  )
}



export async function GetChains(
  data: {
    count: number,
    page_number: number,
    owner_id: string | null
    chain_status: ChainStates | null
}) {
  return await useApi<ChainListResponse>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/chains/list`,
      {
        method: "post",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      },
    )
  )
}




export async function GetChain(chainId: string) {
  return await useApi<ChainClientResponse>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/chains/${chainId}`,
      {
        method: "get",
        headers: {
          'Content-Type': 'application/json',
        },
      },
    )
  )
}


export async function DeleteChain(chainId: number) {
  return await deleteDataUseApi(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/chains/${chainId}`,
      {
        method: "delete",
        headers: {
          'Content-Type': 'application/json',
        },
      },
    )
  )
}


export async function CreateClient(data: {
  chain_id: string,
  password: string | null
  }) {
  return await useApi<ChainResponse>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/chains/client`,
      {
        method: "post",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      },
    )
  )
}



export async function DeleteClient(data: {
  chain_id: string,
  client_id: number
  }) {
  return await deleteDataUseApi(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/chains/client`,
      {
        method: "delete",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      },
    )
  )
}


export async function DownloadFile(
  data: {
    client_id: number,
    chain_id: string
  }
) {
  return await downloadFileUseApi(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/chains/download`,
      {
        method: "post",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      
      },
    )
  )
}


export async function GetMe() {
  return await useApi<User>(
    new Request(
      `${process.env.BACKEND_URL}/api/v1/auth/me`,
      {
        method: "get",
        headers: {
          'Content-Type': 'application/json',
        },
      },
    )
  )
}
