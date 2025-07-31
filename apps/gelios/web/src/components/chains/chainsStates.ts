export type ChainStates = 
  "PENDING_FIRST_STARTUP" | 
  "READY" | 
  "PENDING_ARCHIVED" | 
  "ARCHIVED" |
  "CREATE_CLIENT" | 
  "REVOKE_CLIENT"


export const chainStatusMap: Record<ChainStates, string> = {
  PENDING_FIRST_STARTUP: 'Настройка цепочки',
  ARCHIVED: "Удалена",
  PENDING_ARCHIVED: "Удаление цепочки",
  READY: "Готова к использованию",
  CREATE_CLIENT: "Создание клиента",
  REVOKE_CLIENT: "Удаление клиента"
}

export interface StyleChainStateTag {
  icon: React.ReactNode,
  color: string
}

