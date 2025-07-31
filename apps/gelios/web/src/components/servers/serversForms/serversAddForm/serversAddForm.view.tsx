import React from 'react';
import { Spin } from 'antd';
import { useAsyncFn } from 'react-use';
import { useRouter } from 'next/router';
import { AddServer } from '@/api/gelios.api';
import { ServerFormData } from '../serversForms.type';
import { notifications } from '@/public/notifications';
import { countriesData } from '@/public/country/countriesData';
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
  notification
} from 'antd';


const { Option } = Select;


export function AddServersForm(): React.ReactElement {

  const router = useRouter()
  const [form] = Form.useForm<ServerFormData>();


  const onResetForm = () => {
    form.resetFields();
  };

  
  const [addServerState, addServerCallback] = useAsyncFn(
    async function addServersFn(data: {
      created_data: {
        name: string,
        login: string,
        password: string,
        ip: string,
        country: string
      }
    }) {
      const addServerResponse = await AddServer(data)
      return addServerResponse
    }
  )


  async function addServer(formData: ServerFormData) {
    const addServerResponse = await addServerCallback({
      created_data: {
        name: formData.name,
        login: formData.login,
        password: formData.password,
        ip: formData.ip,
        country: formData.country
      } 
    })
    if (addServerResponse.error) {
      notification.error(notifications.server.addServerError);
      return
    }
    form.resetFields();
    notification.success(notifications.server.addServerSuccess);
  }

  return (
    <>
      <Spin 
        spinning={addServerState.loading} 
        tip={"Подождите, идёт проверка подключения к серверу ..."}>
        <Row>
          <Col span={18}>
            <Row>
              <Col flex="auto">
                <h1>Введите информацию о сервере</h1>
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
                onFinish={addServer}
                autoComplete='off'
              >
                <Form.Item 
                  name="name"
                  label="Название сервера"
                  rules={[{ required: true, message: 'Пожалуйста, введите название сервера'  }]}>
                  <Input />
                </Form.Item>
                <Form.Item 
                  name="login"
                  label="Логин для авторизации"
                  rules={[{ required: true, message: 'Пожалуйста, введите логин для авторизации' }]}>
                  <Input />
                </Form.Item>
                <Form.Item 
                  name="password"
                  label="Пароль для авторизации"
                  rules={[{ required: true, message: 'Пожалуйста, введите пароль для атворизации'}]}>
                  <Input.Password />
                </Form.Item>
                <Form.Item 
                  name="ip"
                  label="IP-адрес сервера"
                  rules={[{ required: true, message: 'Пожалуйста, введите IP-адрес сервера' }]}>
                  <Input />
                </Form.Item>
                <Form.Item
                  name="country"
                  label="Страна расположения сервера"
                  rules={[{ required: true, message: 'Пожалуйста, выберите страну' }]}
                >
                  <Select>
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
                    >
                      Сохранить данные о сервере
                    </Button>
                    <Button 
                      size='large' 
                      type='primary'
                      onClick={onResetForm} 
                      htmlType='button'
                      style={resetFormButtonStyle}
                    >
                      Сбросить данные формы
                    </Button>
                  </Space>
                </Form.Item>
              </Form>
            </ConfigProvider>
          </Col>
        </Row>
      </Spin>
    </>
  );
}