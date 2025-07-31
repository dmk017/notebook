export type ServerStates = 
  "PENDING_FIRST_STARTUP" | 
  "PENDING_LOAD_CHAIN" | 
  "ARCHIVED" | 
  "READY" | 
  "BUSY" | 
  "UNAVAILABLE"


export const serverStatusMap: Record<ServerStates, string> = {
  PENDING_LOAD_CHAIN: 'Ожидание настройки цепочки',
  ARCHIVED: "Удалён",
  PENDING_FIRST_STARTUP: "Подключение к серверу",
  READY: "Готов к использованию",
  BUSY: "Используется в цепочке",
  UNAVAILABLE: "Недоступен",
}



export interface StyleServerStateTag {
  icon: React.ReactNode,
  color: string
}

