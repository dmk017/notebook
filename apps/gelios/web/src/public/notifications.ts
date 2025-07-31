export const notifications = {
  server: {
    addServerError: {
      message: "Ошибка добавления сервера",
      description: "Попробуйте повторить процесс добавления сервера позже",
      duration: 3,
    },
    addServerSuccess: {
      message: "Сервер успешно добавлен",
      description: "Новый сервер был успешно добавлен в ваш список",
      duration: 3,
    },
    getServerError: {
      message: "Ошибка получения данных сервера",
      description: "Сервера не существует",
      duration: 3,
    },
    changeServerError: {
      message: "Ошибка изменения сервера",
      description: "Произошла ошибка при обновлении сервера",
      duration: 3,
    },
    changeServerSuccess: {
      message: "Сервер успешно обновлен",
      description: "Обновлена информация о сервере",
      duration: 3,
    },
    deleteServerError: {
      message: "Ошибка удаления сервера",
      description: "Не удалось удалить сервер. Пожалуйста, попробуйте снова.",
      duration: 3,
    },
    deleteServerSuccess: {
      message: "Сервер успешно удален",
      description: "Сервер добавлен в архив",
      duration: 3,
    },
    transferServerError: {
      message: "Ошибка передачи сервера",
      description: "Не удалось передать выбранный сервер. Пожалуйста, попробуйте снова.",
      duration: 3,
    },
    transferServerSuccess: {
      message: "Сервер успешно передан",
      description: "Сервер был передан выбранному вами пользователю",
      duration: 3,
    },
    getServersError: {
      message: "Ошибка получения серверов",
      description: "Возникла ошибка в получении списка серверов. Пожалуйста, попробуйте снова.",
      duration: 3,
    },
  },
  chain: {
    addChainError: {
      message: "Ошибка при создании цепочки",
      description: "Произошла ошибка. Пожалуйста, попробуйте позже",
      duration: 3,
    },
    addChainSuccess: {
      message: "Цепочка успешно создана",
      description: "Цепочка добавлена в ваш список",
      duration: 3,
    },
    getChainsError: {
      message: "Ошибка получения цепочек",
      description: "Произошла ошибка. Пожалуйста, попробуйте позже",
      duration: 3,
    },
    deleteChainError: {
      message: "Ошибка удаления цепочки",
      description: "Произошла ошибка. Пожалуйста, попробуйте позже",
      duration: 3,
    },
    deleteChainSuccess: {
      message: "Цепочка успешно удалена",
      description: "Цепочка удалена из вашего списка",
      duration: 3,
    },
    getChainError: {
      message: "Ошибка получения цепочки",
      description: "Произошла ошибка. Пожалуйста, попробуйте позже",
      duration: 3,
    },
    createClientError: {
      message: "Ошибка создания клиента",
      description: "Произошла ошибка. Пожалуйста, попробуйте позже",
      duration: 3,
    },
    createClientSuccess: {
      message: "Клиент успешно создан",
      description: "Для продолжения работы скачайте конфигурационный файл клиента",
      duration: 3,
    },
    deleteClientSuccess: {
      message: "Клиент успешно удален",
      description: "Выбранный клиент удален из вашего списка",
      duration: 3,
    },
    deleteClientError: {
      message: "Ошибка удаления клиента",
      description: "Произошла ошибка. Пожалуйста, попробуйте позже",
      duration: 3,
    },
    downloadClientError: {
      message: "Ошибка скачивания клиента",
      description: "Произошла ошибка. Пожалуйста, попробуйте позже",
      duration: 3,
    },
    downloadClientSuccess: {
      message: "Клиент успешно скачан",
      description: "Конфигурационный файл выбранного клиента успешно скачан",
      duration: 3,
    },
  },
  users: {
    getUsersError: {
      message: "Ошибка получения пользователей",
      description: "Не удалось занрузить пользователей текущего модуля системы",
      duration: 3,
    },
  },
};
