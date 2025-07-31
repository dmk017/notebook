import { ChainStates } from "@/components/chains/chainsStates";
import { ServerStates } from "@/components/servers/serversStates";



export interface User {
  user_id: string;
  user_name: string;
  role: "ADMIN" | "USER";
}



// Interfaces for users
export interface UserData {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
}


export interface GroupUsers {
  users: UserData[];
  count: number
}


// Interfaces for servers
export interface ServerInfo {
    id: number;
    name: string;
    country: string;
    login: string;
    ip: string;
    password: string;
    status: ServerStates;
    owner_id: string
}


export interface ServerBaseResponse {
  server_info: ServerInfo,
  owner_info: UserData | null
}


export interface ServerListResponse {
  data: ServerBaseResponse[],
  count: number,
  page_number: number,
  total: number
}


// Interfaces for chains
export interface ChainInfo {
  id: number,
  name: string
  status: ChainStates
  owner_id: string
}

export interface ChainResponse {
  chain_info: ChainInfo
}


export interface ServerData {
  ip: string,
  name: string,
  country: string
}

export interface ChainServersResponse extends ChainResponse {
  servers_info: ServerData[],
  owner_info: UserData | null
}

export interface ChainListResponse {
  data: ChainServersResponse[],
  count: number,
  page_number: number,
  total: number
}


export interface ChainClientInfo {
  id: number,
  client_name: string,
  creator_info: UserData | null
  created_at: string
  password: string | null
}

export interface ChainClientResponse extends ChainServersResponse {
  clients_info:  ChainClientInfo[]
}

