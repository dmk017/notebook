import type { TableProps } from 'antd';
import { useAsyncFn } from 'react-use';
import { useRouter } from 'next/router';
import { useUser } from '@/context/UserContext';
import { SmileOutlined } from '@ant-design/icons';
import { notifications } from '@/public/notifications';
import { AddChainFormData } from './chainsAddFormData';
import { AddChain, GetServers } from '@/api/gelios.api';
import React, { useEffect, useRef, useState } from 'react';
import { countriesData } from '@/public/country/countriesData';
import { ServerStates } from '@/components/servers/serversStates';
import { DEFAULT_PAGE_NUMBER, MAX_INTEGER } from '@/public/constants';
import { TableCellsType, TableCellType } from '@/components/servers/servers.type';
import { resetFormButtonStyle, toListOfChainsButtonStyle } from './chainsAddForm.style';

import { 
  ConfigProvider, 
  Divider, 
  Form, 
  Space, 
  Col, 
  Row,
  Alert,
  Table,
  Timeline,
  Card,
  Image,
  Input,
  Button,
  Spin,
  notification
} from 'antd';


export function ChainsForm(): React.ReactElement {

  const user = useUser();
  const router = useRouter()
  const isInitialMount = useRef(true);
  const [form] = Form.useForm<AddChainFormData>();
  
  const [selectedItems, setSelectedItems] = useState<TableCellType[]>([]);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);

  const rowSelection = {
    onChange: (newSelectedRowKeys: React.Key[], newSelectedItems: TableCellType[]) => {
      setSelectedItems(newSelectedItems)
      setSelectedRowKeys(newSelectedRowKeys)
    },
  };


  const onReset = () => {
    form.resetFields();
    setSelectedItems([])
    setSelectedRowKeys([])
  };


  const [addChainState, addChainCallback] = useAsyncFn(
    async function addChainFn(data: {
      name: string,
      servers_ids: number[]
    }) {
      const addServerResponse = await AddChain(data)
      return addServerResponse
    }
  )


  const [getReadyServersState, getReadyServersCallback] = useAsyncFn(
    async function getReadyServersFn(data: {
      server_status: ServerStates | null,
      owner_id: string | null,
      count: number,
      page_number: number
    }) {
      const serversResponse = await GetServers(data)
      if (serversResponse.error) {
        return serversResponse
      }
      const resultServersData: TableCellsType = {
        data: {
          count: serversResponse.data.count,
          page_number: serversResponse.data.page_number,
          total: serversResponse.data.total,
          data: serversResponse.data.data.map((serverData) => ({
              key: serverData.server_info.id,
              name: serverData.server_info.name,
              country: serverData.server_info.country,
              ip: serverData.server_info.ip,
              status: serverData.server_info.status,
              owner: serverData.owner_info ? `${serverData.owner_info.first_name} ${serverData.owner_info.last_name}` : null
          }))        
        },
        error: null
      }
      return resultServersData
    }
  )


  async function addChain(formData: AddChainFormData) {
   const addChainResponse = await addChainCallback({
        name: formData.name,
        servers_ids: selectedRowKeys.map(Number)
      }
    )
    if (addChainResponse.error) {
      notification.error(notifications.chain.addChainError)
      return
    }
    await getServersList(user?.user_id)
    onReset()
    notification.success(notifications.chain.addChainSuccess)
  }


  async function getServersList(chooseUser: string | undefined = undefined) {
    const getReadyServersResponse = await getReadyServersCallback({
      page_number: DEFAULT_PAGE_NUMBER - 1,
      count: MAX_INTEGER,
      owner_id: chooseUser ?? null,
      server_status: "READY"
    })
    if (getReadyServersResponse.error) {
      notification.error(notifications.server.getServersError)
      return
    }
  }


  const columns: TableProps<TableCellType>['columns'] = [
    {
      title: 'Название',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Страна',
      key: 'country',
      render: (_, record) => (
        <Space>
          <Image
            preview={false}
            src={`/country/flags/${record.country}.svg`}
            height={24}
            width={24}
            alt={`Country Flag ${record.country}`}
          />
          <p>
            {countriesData.find((function(item) {  
              return item.code == record.country  
              }))?.name ?? "Неизвестная страна"
            }
          </p>
        </Space>
      )
    },
    {
      title: 'IP-адрес',
      dataIndex: 'ip',
      key: 'ip',
    },
  ];


  useEffect(() => {
    const fetchData = async () => {
      await getServersList(user?.user_id);
    };
    if (isInitialMount.current && user) {
      isInitialMount.current = false;
      fetchData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);


  return (
    <>
    <Spin 
      spinning={ 
        user === null ||
        getReadyServersState.loading || 
        addChainState.loading 
      } 
      tip={
        addChainState.loading ? "Происходит настройка цепочки. Это может занять несколько минут..." :
        "Поиск серверов..." 
        
      }
    >
      <Row>
        <Col flex="auto">
            <Space direction="vertical">
              <h1>Выберите сервера, которые вы хотите добавить в цепочку</h1>
                <Alert
                  description="Не добавляйте в цепочку больше 3-х серверов. Это может привести к низкой скорости соединения. На данный момент ограничено одним сервером🙈."
                  type="info"
                  showIcon
              />
          </Space>
        </Col>
        <Col flex="100px">
          <Button
            type="primary"
            style={toListOfChainsButtonStyle}
            size='large'
            onClick={() => router.push('/chains')}
          >
            К списку цепочек
          </Button>
        </Col>
      </Row>
      <Divider></Divider>

      {getReadyServersState.value?.data &&
        <Row gutter={32}>
          <Col span={12}>
            <ConfigProvider
              theme={{
                components: {
                  Table: {
                    headerBorderRadius: 10,
                    cellFontSize: 17,
                    headerBg: '#eceff1'
                  },
                },
              }}
            >
              <Table 
                locale={{emptyText() {
                  return <div style={{ textAlign: 'center' }}>
                    <SmileOutlined style={{ fontSize: 20 }} />
                    <p>Нет серверов, готовых к добавлению в цепочку</p>
                  </div>
                },}}
                rowSelection={
                  {
                    type: "checkbox",
                    selectedRowKeys,
                    ...rowSelection,
                  }
                }
                columns={columns} 
                dataSource={getReadyServersState.value.data.data} 
                bordered 
              />
            </ConfigProvider>
          </Col>
          <Col span={12}>
            <Card 
              styles= {{header: {backgroundColor: '#eceff1'} }} 
              title="Выбранные сервера"
            >
              <Form
                form={form}
                autoComplete='off'
                layout="horizontal"
                onFinish={addChain}
              >
                <Form.Item 
                  label="Название цепочки"
                  name="name"
                  rules={[{ required: true, message: "Введите название цепочки" }]} 
                >
                  <Input/>
                </Form.Item>

                {selectedItems.length > 0 && 
                  <Timeline
                    mode='left'
                    items={
                      selectedItems.map((server) => (
                          {
                            children:  (
                              <Space>
                                <Image
                                  preview={false}
                                  src={`/country/flags/${server.country}.svg`}
                                  height={24}
                                  width={24}
                                  alt={`Country Flag ${server.country}`}
                                />
                                {countriesData.find((function(item) {  
                                  return item.code == server.country  
                                  }))?.name ?? "Неизвестная страна"
                                } ({server.ip})
                              </Space>
                            )
                          }
                        )
                      )
                    }
                  /> 
                }
                <Form.Item>
                  <Space>
                    <Button 
                      size='large' 
                      type="primary" 
                      htmlType='submit'
                      disabled={selectedItems.length === 0 || selectedItems.length > 1} //TODO: пока что максимальная длина равна 1}
                    >
                      Добавить цепочку
                    </Button>
                    <Button 
                      size='large' 
                      type='primary'
                      onClick={onReset} 
                      style={resetFormButtonStyle}
                      htmlType='button'
                    >
                      Сбросить данные формы
                    </Button>
                  </Space>
                </Form.Item>
              </Form>
            </Card>
          </Col>
        </Row>
      }
    </Spin>
  </>
);
}