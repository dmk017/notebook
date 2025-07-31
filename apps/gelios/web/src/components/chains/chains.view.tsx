import { useAsyncFn } from 'react-use';
import { useRouter } from 'next/router';
import type { SelectProps } from 'antd';
import { useEffect, useRef, useState } from 'react';
import { useUser } from "../../context/UserContext";
import { notifications } from '@/public/notifications';
import { ChainList, ChainServers } from './chains.type';
import { countriesData } from '@/public/country/countriesData';
import { DeleteChain, GetChains, GetGeliosUsers } from '@/api/gelios.api';
import { ChainStates, StyleChainStateTag, chainStatusMap } from './chainsStates';
import { addChainButtonStyle, chainCardStyle, stylesForSelectField } from './chains.style';

import { 
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  SyncOutlined,
  DeleteOutlined,
  FileOutlined,
  FrownTwoTone
} from '@ant-design/icons';

import {
  Card,
  Row,
  Col, 
  Button, 
  Divider, 
  Typography, 
  Space, 
  Tooltip, 
  Steps, 
  Spin, 
  Tag, 
  Image,
  Modal,
  Select,
  Result,
  notification
} from 'antd'
import { DEFAULT_PAGE_NUMBER, MAX_INTEGER } from '@/public/constants';


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


const { Paragraph } = Typography;
const { Title } = Typography;


export function ChainsPage(): React.ReactElement {
  const user = useUser();
  const isAdmin = user?.role === "ADMIN"

  const router = useRouter()
  const isInitialMount = useRef(true);

  const [chooseUserState, setChooseUserState] = useState<string | undefined>(undefined);
  const [chooseChainState, setChooseChainState] = useState<ChainStates | undefined>(undefined);

  const [isDeleteChainModalVisible, setIsDeleteChainModalVisible] = useState<boolean>(false); 
  const [remoteChainData, setRemoteChain] = useState<ChainServers | null>(null)


  const [getChainsState, getChainsCallback] = useAsyncFn(
    async function getChainsFn(data: {
      chain_status: ChainStates | null,
      owner_id: string | null,
      count: number,
      page_number: number
    }) {
      const chainsResponse = await GetChains(data)
      if (chainsResponse.error) {
        return chainsResponse
      }
      const resultChainsResponse: ChainList = {
        data: {
          count: chainsResponse.data.count,
          page_number: chainsResponse.data.page_number,
          total: chainsResponse.data.total,
          data: chainsResponse.data.data.map((chainData) => ({
              key: chainData.chain_info.id,
              name: chainData.chain_info.name,
              status: chainData.chain_info.status,
              owner: chainData.owner_info ? `${chainData.owner_info.first_name} ${chainData.owner_info.last_name}` : null,
              servers: chainData.servers_info.map((serverData) => ({
                  ip: serverData.ip,
                  name: serverData.name,
                  country: serverData.country
              }))
          }))
        },
        error: null
      }
      return resultChainsResponse
    }
  )


  const [getUsersState, getUsersCallback] = useAsyncFn(
    async function getUsersFn() {
      const geliosUsersResponse = await GetGeliosUsers()
      return geliosUsersResponse
    }
  )


  const [deleteChainState, deleteChainCallback] = useAsyncFn(
    async function deleteChainFn(chainId: number) {
      const deleteChainResponse = await DeleteChain(chainId)
      return deleteChainResponse
    }
  )


  async function getChainsList(
    chainStatus: ChainStates | undefined = undefined,
    chooseUser: string | undefined = undefined
  ) {
    const getChainsResponse = await getChainsCallback({
      page_number: DEFAULT_PAGE_NUMBER - 1,
      count: MAX_INTEGER,
      owner_id: chooseUser ?? null,
      chain_status: chainStatus ?? null,
    })
    if (getChainsResponse.error) {
      notification.error(notifications.chain.getChainsError)
      return
    }
  }


  async function deleteChain(chainId: number) {
    setIsDeleteChainModalVisible(false)
    setRemoteChain(null)
    const deleteChainResponse = await deleteChainCallback(chainId)
    if (deleteChainResponse.error) {
      notification.error(notifications.chain.deleteChainError)
      return
    }
    await getChainsList(chooseChainState, chooseUserState)
    notification.success(notifications.chain.deleteChainSuccess)
  }


  async function onClickChooseUser(userId: string | undefined) {
    setChooseUserState(userId)
    await getChainsList(chooseChainState, userId)
  }

  async function onClickChooseChainState(chainStatus: ChainStates | undefined) {
    setChooseChainState(chainStatus)
    await getChainsList(chainStatus, chooseUserState)
  }


  const usersOptions: SelectProps['options'] = getUsersState.value?.data?.users.map((value) => ({
    "value": value.id,
    "label": `${value.first_name} ${value.last_name}`,
  }))


  const chainStateOptions: SelectProps['options'] = Object.entries(chainStatusMap).map(([value, label]) => ({
    "value": value,
    "label": label
  }))


  function clickOnGetClients(chainId: number): void {
    router.push(`chains/${chainId}`)
  }


  function getModalChainDeletionWindow(chain: ChainServers): void {
    setIsDeleteChainModalVisible(true)
    setRemoteChain(chain)
  }


  function isDisabledButton(chainStatus: ChainStates): boolean {
    return !["READY"].includes(chainStatus)
  }

  
  function isDisabledInfoButton(chainStatus: ChainStates): boolean {
    return ["ARCHIVED"].includes(chainStatus)
  }


  async function generatePage() {
    if (isAdmin) {
      const getUsersResponse = await getUsersCallback();
      if (getUsersResponse.error) {
        notification.error(notifications.users.getUsersError)
        return
      }
    }
    await getChainsList(undefined, user?.user_id);
  }    


  useEffect(() => {
    const fetchData = async () => {
      setChooseUserState(user?.user_id)
      await generatePage()
    }
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
          getChainsState.loading || 
          deleteChainState.loading || 
          getUsersState.loading
        } 
        tip={
          deleteChainState.loading ? "Удаление цепочки..." :
          "Поиск цепочек..."
        }
      >
        <Row>
          <Col flex="auto">
            <h1>Список цепочек серверов</h1>
          </Col>    
          <Col flex="100px">
            <Button
              type="primary"
              style={addChainButtonStyle}
              size='large'
              onClick={() => router.push('/chains/add')}
            >
              Создать цепочку
            </Button>
          </Col>
        </Row>
        <Divider></Divider>

        {getChainsState.value?.data && (
          <>
            <Space wrap>
              <Select
                  allowClear
                  value={chooseChainState}
                  style={stylesForSelectField}
                  placeholder="Выберите статус цепочки"
                  onChange={onClickChooseChainState}
                  options={chainStateOptions}
                />
              {isAdmin && (
                <Select
                  allowClear
                  value={chooseUserState}
                  style={stylesForSelectField}
                  placeholder="Выберите пользователя" 
                  onChange={onClickChooseUser}
                  options={usersOptions}
                /> 
              )}
            </Space>
            {getChainsState.value.data.data.length > 0 ?
              <Row gutter={[24, 48]}>
                {getChainsState.value.data.data.map((chain) => (
                  <Col span={12} key={chain.key}>
                    <Card 
                      style={chainCardStyle}
                      type='inner' 
                      title={
                        <Title 
                          level={5} 
                          style={{ margin: 0 }}
                        >
                          Название цепочки: {chain.name} {chain.owner && `- Создатель: ${chain.owner}`} 
                        </Title> 
                      }
                      extra={
                        <Space> 
                          <Tag 
                            color={chainStatusColorMap[chain.status].color}
                            icon={chainStatusColorMap[chain.status].icon}
                          >
                            {chainStatusMap[chain.status]}
                          </Tag>
                          <Tooltip key="ovpn_files" title="VPN-файлы">
                            <Button
                              disabled={isDisabledInfoButton(chain.status)}
                              icon={<FileOutlined />}
                              type='primary'
                              onClick={() => clickOnGetClients(chain.key)}
                            />
                          </Tooltip>
                          <Tooltip key="delete" title="Удалить цепочку">
                            <Button
                              disabled={isDisabledButton(chain.status)}
                              icon={<DeleteOutlined />}
                              type='primary'
                              danger
                              onClick={() => getModalChainDeletionWindow(chain)}
                            />
                          </Tooltip>
                        </Space>
                      }
                    >
                      <Steps
                        size="small"
                        labelPlacement="vertical"
                        current={chain.servers.length - 1}
                        items={
                          chain.servers.map((server) => ({
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
                      />
                    </Card>
                  </Col>
                ))}
              </Row>
              :
              <Result
                icon={<FrownTwoTone/>}
                title="Пока что нет таких VPN-цепочек"
              />
            }
          </>
        )}
      </Spin>
      <Modal 
        title="Вы действительно хотите удалить цепочку?"
        open={isDeleteChainModalVisible} 
        okText="Да"
        cancelText="Нет"
        onOk={() => 
          {
            deleteChain(remoteChainData?.key ?? -1)}
          } 
        onCancel={() => { 
          setIsDeleteChainModalVisible(false); 
          setRemoteChain(null)
        }}
      > 
        <Paragraph>
          <pre>
            {remoteChainData?.owner && (<>Владелец цепочки - {remoteChainData.owner}<br/></>)}
            Название цепочки - {remoteChainData?.name}<br/>
            Статус цепочки - {remoteChainData?.status && chainStatusMap[remoteChainData?.status]}  
          </pre>
        </Paragraph>
      </Modal>
    </>    
  )
}