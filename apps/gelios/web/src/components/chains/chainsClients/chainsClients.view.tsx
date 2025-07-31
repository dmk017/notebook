
import { format } from 'date-fns';
import { useAsyncFn } from 'react-use';
import { useRouter } from 'next/router';
import { ChainClientInfo } from '@/api/gelios.types';
import { notifications } from '@/public/notifications';
import React, { useEffect, useRef, useState } from 'react';
import { countriesData } from '@/public/country/countriesData';
import { ChainStates, StyleChainStateTag, chainStatusMap } from '../chainsStates';
import { CreateClient, DeleteClient, DownloadFile, GetChain } from '@/api/gelios.api';

import { 
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  SyncOutlined,
  PlusOutlined,
  DownloadOutlined,
  SmileOutlined,
  DeleteOutlined
} from '@ant-design/icons';

import { 
  Spin, 
  Steps, 
  Image, 
  Collapse, 
  Space, 
  Tag, 
  Tooltip, 
  Button, 
  Row, 
  Col, 
  Divider, 
  List, 
  Avatar, 
  notification, 
  Result, 
  Modal, 
  Typography, 
  Input 
} from 'antd';


const { Paragraph } = Typography;


const chainStatusColorMap: Record<ChainStates, StyleChainStateTag> = {
  ARCHIVED: {
    color: "warning",
    icon: <ExclamationCircleOutlined />
  },
  PENDING_FIRST_STARTUP: {
    color: 'processing',
    icon: <SyncOutlined spin />
  },
  READY: {
    color: "success",
    icon: <CheckCircleOutlined />
  },
  PENDING_ARCHIVED: {
    color: "processing",
    icon: <SyncOutlined spin/>
  },
  CREATE_CLIENT: {
    color: "processing",
    icon: <SyncOutlined spin/>
  },
  REVOKE_CLIENT: {
    color: "processing",
    icon: <SyncOutlined spin/>
  },
}


export function ChainClientsData(): React.ReactElement {

  const router = useRouter()
  const isInitialMount = useRef(true);



  const [isDeleteClientModalVisible, setisDeleteClientModalVisible] = useState<boolean>(false); 
  const [deleteClientData, setDeleteClient] = useState<ChainClientInfo | null>(null);

  const [isCreateClientModalVisible, setIsCreateClientModalVisible] = useState<boolean>(false); 
  const [password, setPassword] = useState<string>('');


  const [getChainState, getChainCallback] = useAsyncFn(
    async function getChainsFn(chainId: string) {
      const getChainResponse = await GetChain(chainId)
      return getChainResponse
    }
  )


  const [createClientState, createClientCallback] = useAsyncFn(
    async function createClientFn(data: {
        chain_id: string,
        password: string | null
    }) {
      const createClientResponse = await CreateClient(data)
      return createClientResponse
    }
  )


  const [deleteClientState, deleteClientCallback] = useAsyncFn(
    async function deleteClientFn(data: {
        chain_id: string,
        client_id: number
    }) {
      const deleteClientResponse = await DeleteClient(data)
      return deleteClientResponse
    }
  )


  const [downloadClientState, downloadClientCallback] = useAsyncFn(
    async function downloadClientFn(data: {
        chain_id: string,
        client_id: number
    }) {
      const downloadClientResponse = await DownloadFile(data)
      return downloadClientResponse
    }
  )


  async function getChain(chainId: string) {
    const getChainResponse = await getChainCallback(chainId)
    if (getChainResponse.error) {
      notification.error(notifications.chain.getChainError)
      return
    }
  }


  async function createClient(password: string | null) {
    setIsCreateClientModalVisible(false)
    setPassword("")
    const createClientResponse = await createClientCallback({
      chain_id: router.query?.id?.toString?.() ?? "",
      password: password
    })
    if (createClientResponse.error) {
      notification.error(notifications.chain.createClientError)
      return
    }
    await getChain(router.query?.id?.toString?.() ?? "")
    notification.success(notifications.chain.createClientSuccess)
  }


  async function deleteClient(client_id: number) {
    setisDeleteClientModalVisible(false); 
    setDeleteClient(null)
    const deleteClientResponse = await deleteClientCallback({
      chain_id: router.query?.id?.toString?.() ?? "",
      client_id: client_id
    })
    if (deleteClientResponse.error) {
      notification.error(notifications.chain.deleteClientError)
      return
    }
    await getChain(router.query?.id?.toString?.() ?? "")
    notification.success(notifications.chain.deleteClientSuccess)
  }


  async function downloadClient(client_id: number) {
    const downloadClientResponse = await downloadClientCallback({
      chain_id: router.query?.id?.toString?.() ?? "",
      client_id: client_id
    })
    if (downloadClientResponse.error) {
      notification.error(notifications.chain.downloadClientError)
      return
    }
    notification.success(notifications.chain.downloadClientSuccess)
  }
  

  function getModalDeleteClientWindow(client: ChainClientInfo): void {
    setisDeleteClientModalVisible(true)
    setDeleteClient(client)
  }


  function getModalCreateClientWindow(): void {
    setIsCreateClientModalVisible(true)
  }


  function isDisabledButton(chainStatus: ChainStates): boolean {
    return !["READY"].includes(chainStatus)
  }
  

  useEffect(() => {
    if (router.isReady && isInitialMount.current) {
      isInitialMount.current = false; 
      const fetchData = async () => {
        await getChain(router.query?.id?.toString?.() ?? "");
      };
      fetchData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router.isReady])
        
  return (
    <>
      <Spin 
        spinning={
          getChainState.loading || 
          createClientState.loading || 
          deleteClientState.loading || 
          downloadClientState.loading
        } 
        tip={getChainState.loading ? "Получаем данные о цепочке..." :
            createClientState.loading ? "Создание клиента..." :
            deleteClientState.loading ? "Удаление клиента..." :
            "Скачивание конфигурационного файла..."}>
        <Row>
          {getChainState.value?.data &&
          <Col span={18}>
            <Row>
              <Col flex="auto">
                <h1>Список клиентов цепочки - {getChainState.value.data.chain_info.name}</h1>
              </Col>    
              <Col flex="100px">
                <Button
                  type="primary"
                  style={{backgroundColor: '#778899'}}
                  size='large'
                  onClick={() => router.push('/chains')}
                >
                  К списку цепочек
                </Button>
              </Col>
            </Row>
            <Divider></Divider>
            <Collapse defaultActiveKey={['1']}
              items={
                [{ 
                  key: '1',
                  label:  
                    <Steps
                      size="small"
                      labelPlacement="vertical"
                      current={getChainState.value.data.servers_info.length - 1}
                      items={
                        getChainState.value.data.servers_info.map((server) => ({
                          title: server.name,
                          icon: ( 
                            <Image
                              preview={false}
                              src={`/country/flags/${server.country}.svg`}
                              height={24}
                              width={24}
                              alt={`Country Flag ${server.country}`}
                            />
                          ),
                          description: (
                            `${countriesData.find((function(item) {  
                              return item.code == server.country  
                              }))?.name ?? "Неизвестная страна"} 
                              ${server.ip}`
                          )
                        }))
                      }
                    />, 
                  extra: 
                    <Space> 
                      <Tag 
                        color={chainStatusColorMap[getChainState.value.data.chain_info.status].color}
                        icon={chainStatusColorMap[getChainState.value.data.chain_info.status].icon}
                      >
                        {chainStatusMap[getChainState.value.data.chain_info.status]}
                      </Tag>
                      <Tooltip key="ovpn_files" title="Создать клиента">
                        <Button
                          disabled={isDisabledButton(getChainState.value.data.chain_info.status)}
                          icon={<PlusOutlined/>}
                          type='primary'
                          size='large'
                          onClick={(event) => {
                            event.stopPropagation();
                            getModalCreateClientWindow()
                          }}
                        />
                      </Tooltip>
                    </Space>,
                  children:
                    <List
                      itemLayout="horizontal"
                      dataSource={getChainState.value.data.clients_info}
                      locale={{ emptyText: 
                        <div style={{ textAlign: 'center' }}>
                          <SmileOutlined style={{ fontSize: 20 }} />
                          <p>Нет созданных клиентов</p>
                        </div>
                      }}
                      renderItem={(item) => (
                        <List.Item
                          actions={[
                            <Tooltip key="ovpn_files" title="Скачать конфигурационный файл">
                              <Button
                                key="download-ovpn-file"
                                disabled={isDisabledButton((
                                  getChainState?.value?.data as NonNullable<typeof getChainState.value.data>).chain_info.status
                                )}
                                icon={<DownloadOutlined />}
                                type='primary'
                                size='large'
                                onClick={() => downloadClient(item.id)}
                              />
                              </Tooltip>,
                            <Tooltip key="ovpn_files" title="Удалить конфигурационный файл">
                            <Button
                              key="delete-ovpn-file"
                              disabled={
                                isDisabledButton((
                                  getChainState?.value?.data as NonNullable<typeof getChainState.value.data>).chain_info.status
                                )}
                              icon={<DeleteOutlined />}
                              type='primary'
                              danger
                              size='large'
                              onClick={() => getModalDeleteClientWindow(item)}
                            />
                            </Tooltip>
                          ]}  
                        >
                          <List.Item.Meta
                            avatar={<Avatar src="/vpnIcon/vpnIcon.svg" />}
                            title={`Название конфигурационного файла: ${item.client_name}`}
                            description={
                              `Создан ${item.creator_info ? `пользователем ${item.creator_info.first_name} ${item.creator_info.last_name}` : ""}  в ${format(new Date(item.created_at), 'HH:mm dd.MM.yyyy')} ${item.password ? `с паролем ${item.password}` : "без пароля"}`}
                          />
                        </List.Item>
                      )}
                    />  
                }]
              }
            />
          </Col>
          } 
          {getChainState.value?.error &&
          <Col span={10} offset={6}>
            <Result
              status="404"
              title="404"
              subTitle="К сожалению, страница, которую вы посетили, не существует."
              extra={<Button type="primary" onClick={() => router.push('/chains')}>К списку цепочек</Button>}
            />
          </Col>
          }
        </Row> 
      </Spin>
      <Modal 
        title="Вы действительно хотите удалить конфигурационный файл?"
        open={isDeleteClientModalVisible} 
        okText="Да"
        cancelText="Нет"
        onOk={() => 
          {
            deleteClient(deleteClientData?.id ?? -1)}
          } 
        onCancel={() => { 
          setisDeleteClientModalVisible(false); 
          setDeleteClient(null)
        }}
      > 
        <Paragraph>
          <pre>
            Название клиента - {deleteClientData?.client_name}<br/>
            Дата добавления - {deleteClientData?.created_at && format(new Date(deleteClientData.created_at), 'HH:mm dd.MM.yyyy')}<br/>
            {deleteClientData?.creator_info && <>Создатель - {deleteClientData?.creator_info.first_name} {deleteClientData?.creator_info.last_name}<br/></>}
            Пароль - {deleteClientData?.password ? deleteClientData.password : "Нет пароля"}  
          </pre>
        </Paragraph>
      </Modal>
      <Modal 
        title="Создайте пароль для конфигурационного файла (не обязательно)"
        open={isCreateClientModalVisible} 
        okText="Создать"
        cancelText="Не создавать"
        okButtonProps={{ disabled: password.length > 0 && password.length < 4  }}
        onOk={() => createClient(password.length > 0 ? password : null)}
        onCancel={() => { 
          setIsCreateClientModalVisible(false);
          setPassword("")
        }}
      > 
        <p>При вводе пароля, он должен составлять не менее 4 символов</p>
        <Paragraph>
        <Input.Password
          placeholder="Введите пароль для создания клиента"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
          }}
        />
        </Paragraph>
      </Modal>
    </>
  );
}