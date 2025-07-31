import { useAsyncFn } from 'react-use';
import { useRouter } from 'next/router';
import React, { useEffect, useRef } from 'react';
import { ServerFormData } from '../serversForms.type';
import  {InfoCircleOutlined } from '@ant-design/icons';
import { notifications } from '@/public/notifications';
import { GetServer, ChangeServer } from '@/api/gelios.api';
import { countriesData } from '@/public/country/countriesData';
import { ServerStates, serverStatusMap } from '../../serversStates';
import { resetFormButtonStyle, toListOfServersButtonStyle } from '../serversForms.style';

import { 
  Button, 
  ConfigProvider, 
  Form, 
  Input, 
  Space, 
  Select,
  Divider, 
  Col, 
  Row,
  Spin,
  Tooltip,
  Result,
  notification
} from 'antd';


const { Option } = Select;


export function ChangeServersForm(): React.ReactElement {

  const router = useRouter()
  const isInitialMount = useRef(true);
  const [form] = Form.useForm<ServerFormData>();


  const onResetForm = () => {
    form.resetFields();
  };


  function isHidden(serverStatus: ServerStates): boolean {
    return !["UNAVAILABLE", "READY"].includes(serverStatus)
  }


  const [getServerState, getServerCallback] = useAsyncFn(
    async function getServerFn(serverId: string) {
      const getServerResponse = await GetServer(serverId)
      return getServerResponse
    }
  )


  const [changeServerState, changeServerCallback] = useAsyncFn(
    async function changeServerFn(
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
      const changeServerResponse = await ChangeServer(data)
      return changeServerResponse
    }
  )


  async function getServer(serverId: string) {
    const response = await getServerCallback(serverId)
    if (response.error) {
      notification.error(notifications.server.getServerError);
      return
    }
  }

  
  async function changeServer(formData: ServerFormData) {
    const changeServerResponse = await changeServerCallback({
      updated_data: {
        name: formData.name,
        login: formData.login,
        password: formData.password,
        ip: formData.ip,
        country: formData.country
      },
      server_id: router.query?.id?.toString?.() ?? ""
    })
    if (changeServerResponse.error) {
      notification.error(notifications.server.changeServerError);
      return
    }
    await getServer(router.query?.id?.toString?.() ?? "")
    notification.success(notifications.server.changeServerSuccess);
  }


  useEffect(() => {
    if (isInitialMount.current && router.isReady) {
        isInitialMount.current = false;
        const fetchData = async () => {
          await getServer(router.query?.id?.toString?.() ?? "");
        };
        fetchData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router.isReady]);
        


  return (
    <>
      <Spin 
        spinning={getServerState.loading || changeServerState.loading} 
        tip={getServerState.loading ? 
            "Получаем данные о сервере" : 
            "Подождите, идёт процесс изменения данных и подключение к серверу"}>
              
        <Row>
          {getServerState.value?.data &&
          <Col span={18}>
            <Row>
              <Col flex="auto">
                <h1>
                  Информация о сервере
                  {isHidden(getServerState.value.data.server_info.status) &&
                      <Tooltip title={`Настройки сервера нельзя изменить, так как он: ${serverStatusMap[getServerState.value.data.server_info.status]}`}>
                        <InfoCircleOutlined style={{ marginLeft: 8 }} />
                      </Tooltip>
                  }
                </h1>
              </Col>
              <Col flex="100px">
                <Button 
                  type="primary"
                  style={toListOfServersButtonStyle}
                  size='large'
                  onClick={() => router.push('/')}
                >
                  К списку серверов
                </Button>
              </Col>
            </Row>
            <Divider></Divider>
            <ConfigProvider
              theme={{
                components: {
                  Form: {
                    labelFontSize: 17
                  },
                },
              }}
            >
              <Form
                layout='vertical'
                form={form}
                name="servers-form"
                onFinish={changeServer}
                autoComplete='off'
                initialValues={
                  {
                    "name": getServerState.value.data.server_info.name,
                    "country": getServerState.value.data.server_info.country,
                    "password": getServerState.value.data.server_info.password,
                    "login": getServerState.value.data.server_info.login,
                    "ip": getServerState.value.data.server_info.ip,
                  }
                }
              >
                <Form.Item 
                  name="name"
                  label="Название сервера"
                  rules={[{ required: true, message: 'Пожалуйста, введите название сервера'  }]}>
                  <Input readOnly={isHidden(getServerState.value.data.server_info.status)} />
                </Form.Item>
                <Form.Item 
                  name="login"
                  label="Логин для авторизации"
                  rules={[{ required: true, message: 'Пожалуйста, введите логин для авторизации' }]}>
                  <Input readOnly={isHidden(getServerState.value.data.server_info.status)}/>
                </Form.Item>
                <Form.Item 
                  name="password"
                  label="Пароль для авторизации"
                  rules={[{ required: true, message: 'Пожалуйста, введите пароль для авторизации'}]}>
                  <Input.Password readOnly={isHidden(getServerState.value.data.server_info.status)}/>
                </Form.Item>
                <Form.Item 
                  name="ip"
                  label="IP-адрес сервера"
                  rules={[{ required: true, message: 'Пожалуйста, введите IP-адрес сервера' }]}>
                  <Input readOnly={isHidden(getServerState.value.data.server_info.status)}/>
                </Form.Item>
                <Form.Item
                  name="country"
                  label="Страна расположения сервера"
                  rules={[{ required: true, message: 'Пожалуйста, выберите страну' }]}
                >
                  <Select style = {{
                    backgroundColor: isHidden(getServerState.value.data.server_info.status) ? '#f5f5f5' : '',
                    borderColor: isHidden(getServerState.value.data.server_info.status) ? '#d9d9d9' : '',
                    pointerEvents: isHidden(getServerState.value.data.server_info.status) ? 'none' : 'auto',
                  }}>
                    {countriesData.map((item, index) => (
                      <Option value={item.code} key={index}>{item.name}</Option>
                      ))}
                  </Select>
                </Form.Item>
                <Form.Item>
                  <Space>
                    <Button 
                      size='large' 
                      type="primary" 
                      htmlType='submit'
                      disabled={isHidden(getServerState.value.data.server_info.status)}
                    >
                      Изменить настройки сервера
                    </Button>
                    <Button 
                      size='large' 
                      type='primary'
                      disabled={isHidden(getServerState.value.data.server_info.status)}
                      onClick={onResetForm} 
                      htmlType='button'
                      style={resetFormButtonStyle}
                    >
                      Вернуться к первоначальным настройкам
                    </Button>
                  </Space>
                </Form.Item>
              </Form>
            </ConfigProvider>
          </Col>
          }
          {getServerState.value?.error && 
          <Col span={10} offset={6}>
            <Result
              status="404"
              title="404"
              subTitle="К сожалению, страница, которую вы посетили, не существует."
              extra={<Button type="primary" onClick={() => router.push('/')}>К списку серверов</Button>}
            />
          </Col>
          }   
        </Row>
      </Spin>
    </>
  );
}