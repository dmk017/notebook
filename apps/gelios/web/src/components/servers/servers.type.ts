import { ServerStates } from "./serversStates";


export interface TableCellType {
  key: number;
  name: string;
  country: string;
  ip: string;
  status: ServerStates;
  owner: string | null
}


export interface TableCellsType {
  data: {
    data: TableCellType[],
    count: number,
    page_number: number,
    total: number
  },
  error: null
}