import React from 'react'
import {
  BulbOutlined,
  CalculatorOutlined,
  DeliveredProcedureOutlined,
  FileTextOutlined,
} from '@ant-design/icons'
import { PrimitiveTypeEnum } from '../../store/main-api/generate/api'

const iconPropertiesStyle: React.CSSProperties = {
  fontSize: '18px',
  color: '#08c',
}

export const propertyPrimitiveTypeMap: Record<
  PrimitiveTypeEnum,
  {
    icon: React.ReactNode
    title: string
  }
> = {
  STR: {
    icon: <FileTextOutlined style={iconPropertiesStyle} />,
    title: 'Строковый',
  },
  BOOL: {
    icon: <BulbOutlined style={iconPropertiesStyle} />,
    title: 'Логический',
  },
  DATE: {
    icon: <DeliveredProcedureOutlined style={iconPropertiesStyle} />,
    title: ' Дата',
  },
  FILE: {
    icon: <DeliveredProcedureOutlined style={iconPropertiesStyle} />,
    title: 'Файл',
  },
  NUMBER: {
    icon: <CalculatorOutlined style={iconPropertiesStyle} />,
    title: 'Числовой',
  },
}

export const propertyValidationMap: Record<
  string,
  {
    icon: React.ReactNode
    title: string
    regex: RegExp
  }
> = {
  DEFAULT: {
    icon: <FileTextOutlined style={iconPropertiesStyle} />,
    title: 'По умолчанию',
    regex: new RegExp('^.{2,}$'),
  },
  FULLNAME: {
    icon: <FileTextOutlined style={iconPropertiesStyle} />,
    title: 'ФИО',
    regex: new RegExp('^[А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23}$'),
  },
  PHONE_NUMBER: {
    icon: <FileTextOutlined style={iconPropertiesStyle} />,
    title: 'Номер телефона (RUS)',
    regex: new RegExp(
      '((8|\\+7)[\\-\\.]?)?(\\(?\\d{3}\\)?[\\-\\.]?)?[\\d\\-\\.]{7,10}'
    ),
  },
  VK_PAGE: {
    icon: <FileTextOutlined style={iconPropertiesStyle} />,
    title: 'Страница ВК',
    regex: new RegExp('^(https?\\:\\/\\/)?(www\\.)?vk\\.com/(\\w|\\d)+?\\/?$'),
  },
  TELEGRAM_CHANNEL: {
    icon: <FileTextOutlined style={iconPropertiesStyle} />,
    title: 'Telegram канал',
    regex: new RegExp('^(https?\\:\\/\\/)?t\\.me/(\\w|\\d)+?\\/?$'),
  },
  TELEGRAM_ACCOUNT: {
    icon: <FileTextOutlined style={iconPropertiesStyle} />,
    title: 'Telegram аккаунт',
    regex: new RegExp('^\\@[A-Za-z\\d_]{5,32}$'),
  },
}
