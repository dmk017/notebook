import { ChainStates } from "./chainsStates";

interface Server {
  ip: string;
  name: string
  country: string;
}

export interface ChainServers {
  key: number;
  name: string;
  status: ChainStates
  owner: string | null
  servers: Server[]
}

export interface ChainList {
  data: {
    data: ChainServers[];
    count: number;
    page_number: number;
    total: number
  }
  error: null
}