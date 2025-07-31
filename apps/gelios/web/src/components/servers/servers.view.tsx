import { useAsyncFn } from 'react-use';
import { useRouter } from 'next/router';
import ruRU from 'antd/lib/locale/ru_RU';
import type { TableProps, SelectProps } from 'antd';
import { useUser } from "../../context/UserContext";
import React, { useState, useEffect, useRef } from 'react';
import {countriesData} from "@/public/country/countriesData"
import { TableCellsType, TableCellType } from './servers.type';
import { DEFAULT_PAGE_SIZE, DEFAULT_PAGE_NUMBER } from '@/public/constants';

import { 
  ServerStates, 
  StyleServerStateTag, 
  serverStatusMap 
} from './serversStates';

import { 
  DeleteServer, 
  GetGeliosUsers, 
  GetServers, 
  UpdateServerOwner 
} from '@/api/gelios.api';

import { 
  addServerButtonStyle, 
  stylesForSelectField, 
  transferServerButtonStyle 
} from './servers.style';

import { 
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  SyncOutlined,
  DeleteFilled,
  UserSwitchOutlined,
  SmileOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';

import { 
  ConfigProvider,
  Space,
  Image,
  Button, 
  Table, 
  Tag, 
  Tooltip, 
  Flex, 
  Divider, 
  Row, 
  Col,
  Modal,
  Typography,
  Select,
  Spin,
  notification,
} from 'antd';
import { notifications } from '@/public/notifications';


const { Paragraph } = Typography;


const serverStatusColorMap: Record<ServerStates, StyleServerStateTag> = {
  PENDING_LOAD_CHAIN: {
    color: 'processing',
    icon: <SyncOutlined spin />
  },
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
  BUSY: {
    color: "success",
    icon: <CheckCircleOutlined />
  },
  UNAVAILABLE: {
    color: "error",
    icon: <CloseCircleOutlined />
  }
}

export function ServersPage(): React.ReactElement {
  const user = useUser();
  const isAdmin = user?.role === "ADMIN"

  const router = useRouter()
  const isInitialMount = useRef(true);

  const [isDeleteServerModalVisible, setIsDeleteServerModalVisible] = useState<boolean>(false); 

  const [isTransferServerModalVisible, setIsTransferServerModalVisible] = useState<boolean>(false); 
  const [serverTransferUserState, setServerTransferUserState] = useState<string | undefined>(undefined);

  const [remoteServerData, setRemoteServer] = useState<TableCellType | null>(null)

  const [chooseServerState, setChooseServersState] = useState<ServerStates | undefined>(undefined);
  const [chooseUserState, setChooseUserState] = useState<string | undefined>(undefined);

  const [currentPage, setCurrentPage] = useState<number>(DEFAULT_PAGE_NUMBER);
  const [pageSize, setPageSize] = useState<number>(DEFAULT_PAGE_SIZE);


  const [getServersState, getServersCallback] = useAsyncFn(
    async function getServersFn(data: {
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
              owner: serverData.owner_info ? `${serverData.owner_info.first_name} ${serverData.owner_info.last_name}` : null,
          }))        
        },
        error: null
      }
      return resultServersData
    }
  )


  const [deleteServerState, deleteServerCallback] = useAsyncFn(
    async function deleteServerFn(serverId: number) {
      const deleteServerResponse = await DeleteServer(serverId)
      return deleteServerResponse
    }
  )


  const [getUsersState, getUsersCallback] = useAsyncFn(
    async function getUsersFn() {
      const geliosUsersResponse = await GetGeliosUsers()
      return geliosUsersResponse
    }
  )


  const [transferServerState, transferServerCallback] = useAsyncFn(
    async function transferServerFn(data: {
        owner_id: string,
        server_id: number
      }
    ) {
      const transferServerResponse = await UpdateServerOwner(data)
      return transferServerResponse
    }
  )


  async function getServersList(
    serverStatus: ServerStates | undefined = undefined,
    chooseUser: string | undefined = undefined,
    page: number = currentPage,
    size: number = pageSize
  ) {
    const getServersResponse = await getServersCallback({
      page_number: page - 1,
      count: size,
      owner_id: chooseUser ?? null,
      server_status: serverStatus ?? null
    })
    if (getServersResponse.error) {
      notification.error(notifications.server.getServersError);
      return
    }
  }


  async function onClickChooseServerState(serverStatus: ServerStates | undefined) {
    setChooseServersState(serverStatus)
    setCurrentPage(DEFAULT_PAGE_NUMBER)
    await getServersList(serverStatus, chooseUserState, DEFAULT_PAGE_NUMBER, pageSize)
  }


  async function onClickChooseUser(userId: string | undefined) {
    setChooseUserState(userId)
    setCurrentPage(DEFAULT_PAGE_NUMBER)
    await getServersList(chooseServerState, userId, DEFAULT_PAGE_NUMBER, pageSize)
  }


  async function deleteServer(serverId: number) {
    setIsDeleteServerModalVisible(false); 
    setRemoteServer(null)
    const deleteServerResponse = await deleteServerCallback(serverId)
    if (deleteServerResponse.error) {
      notification.error(notifications.server.deleteServerError);
      return
    }
    setCurrentPage(DEFAULT_PAGE_NUMBER)
    await getServersList(chooseServerState, chooseUserState, DEFAULT_PAGE_NUMBER, pageSize);
    notification.success(notifications.server.deleteServerSuccess);
  }


  async function transferServer(serverId: number, userId: string) {
    setIsTransferServerModalVisible(false);
    setServerTransferUserState(undefined)
    setRemoteServer(null)
    const transferServerResponse = await transferServerCallback({
      server_id: serverId,
      owner_id: userId
    })
    if (transferServerResponse.error) {
      notification.error(notifications.server.transferServerError);
      return
    }
    setCurrentPage(DEFAULT_PAGE_NUMBER)
    await getServersList(chooseServerState, chooseUserState, DEFAULT_PAGE_NUMBER, pageSize);
    notification.success(notifications.server.transferServerSuccess);
  }


  function clickOnChangeServer(serverId: number) {
    router.push(`servers/${serverId}/info`)
  }


  function isDisabledButton(serverStatus: ServerStates): boolean {
    return !["UNAVAILABLE", "READY"].includes(serverStatus)
  }


  function isDisabledInfoButton(serverStatus: ServerStates): boolean {
    return ["ARCHIVED"].includes(serverStatus)
  }


  function getModalServerDeletionWindow(server: TableCellType): void {
    setIsDeleteServerModalVisible(true)
    setRemoteServer(server)
  }


  function getModalServerTransferWindow(server: TableCellType): void {
    setIsTransferServerModalVisible(true)
    setRemoteServer(server)
  }

  
  const serverStateOptions: SelectProps['options'] = Object.entries(serverStatusMap).map(([value, label]) => ({
    "value": value,
    "label": label
  }))


  const usersOptions: SelectProps['options'] = getUsersState.value?.data?.users.map((value) => ({
    "value": value.id,
    "label": `${value.first_name} ${value.last_name}`,
  }))


  const columns: TableProps<TableCellType>['columns'] = [
    ...(isAdmin ? [{
      title: 'Владелец',
      dataIndex: 'owner',
      key: 'owner',
    }] : []),
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
    {
      title: 'Статус',
      key: 'status',
      render: (_, record) => (
        <Tag 
          color={serverStatusColorMap[record.status].color}
          icon={serverStatusColorMap[record.status].icon}
        >
          {serverStatusMap[record.status]}
        </Tag>
      )  
    },
    {
      title: 'Действие',
      key: 'action',
      render: (_, record)  => (
        <Flex gap="middle">
          <Tooltip title="Удалить">
            <Button
              size='large'
              type="primary" 
              danger
              disabled={isDisabledButton(record.status)}
              icon={<DeleteFilled/>} 
              onClick={() => getModalServerDeletionWindow(record)}
            />
          </Tooltip>
          <Tooltip title="Информация / Изменение настроек">
            <Button 
              size='large'
              type="primary"  
              icon={<InfoCircleOutlined/>} 
              disabled={isDisabledInfoButton(record.status)}
              onClick={() => clickOnChangeServer(record.key)}
            />
          </Tooltip>
          {isAdmin && (
            <Tooltip title="Передать">
              <Button
                type='primary'
                style={transferServerButtonStyle}
                size='large'
                disabled={isDisabledButton(record.status)} 
                icon={<UserSwitchOutlined/>}
                onClick={() => getModalServerTransferWindow(record)}
              />
            </Tooltip>
          )}
        </Flex> 
      ), 
    },
  ];


  const handleTableChange: TableProps<TableCellType>['onChange'] = async (pagination) => {
    const { current = DEFAULT_PAGE_NUMBER, pageSize: newPageSize = DEFAULT_PAGE_SIZE } = pagination;
    setCurrentPage(current);
    setPageSize(newPageSize);
    await getServersList(chooseServerState, chooseUserState, current, newPageSize);
  };


  async function generatePage() {
    if (isAdmin) {
      const getUsersResponse = await getUsersCallback();
      if (getUsersResponse.error) {
        notification.error(notifications.users.getUsersError)
        return
      }
    }
    await getServersList(undefined, user?.user_id, currentPage, pageSize);
  }


  useEffect(() => {
    const fetchData = async () => {
      setChooseUserState(user?.user_id)
      await generatePage()
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
          getServersState.loading || 
          deleteServerState.loading || 
          getUsersState.loading || 
          transferServerState.loading
        } 
        tip={
          deleteServerState.loading ? "Удаление сервера..." :
          transferServerState.loading ? "Передача сервера..." :
          "Поиск серверов..."
        }
      >
        <Row>
          <Col flex="auto">
            <h1>Список серверов</h1>
          </Col>
          <Col flex="100px">
            <Button
              type="primary"
              style={addServerButtonStyle}
              size='large'
              onClick={() => router.push('/servers/add')}
            >
              Добавить сервер
            </Button>
          </Col>
        </Row>
        <Divider></Divider>

        {getServersState.value?.data && 
          <>
            <Space wrap>
              <Select
                allowClear
                value={chooseServerState}
                style={stylesForSelectField}
                placeholder="Выберите статус сервера"
                onChange={onClickChooseServerState}
                options={serverStateOptions}
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

            <ConfigProvider
              locale={{
                ...ruRU,
                Pagination: {
                  ...ruRU.Pagination,
                  items_per_page: ' ',
                }
              }}
              theme={{
                components: {
                  Table: {
                    headerBorderRadius: 10,
                    cellFontSize: 17,
                    headerBg: '#eceff1',
                  },
                },
              }}
            >
              <Table 
                locale={{emptyText() {
                    return <div style={{ textAlign: 'center' }}>
                    <SmileOutlined style={{ fontSize: 20 }} />
                    { chooseServerState ?  
                      (
                        <p>Нет серверов: {serverStatusMap[chooseServerState]}</p>
                      ) : 
                      <p>Нет загруженных серверов</p>
                    }
                  </div>
                },}}
                columns={columns} 
                dataSource={getServersState.value?.data?.data}
                bordered 
                pagination={{
                  current: currentPage,
                  pageSize: pageSize,
                  total: getServersState.value?.data?.total,
                  showSizeChanger: true,
                  pageSizeOptions: ['10', '20', '50', '100'],
                }}
                onChange={handleTableChange}
              />
            </ConfigProvider>
          </>
        }
      </Spin>
      <Modal 
        title="Вы действительно хотите удалить сервер?"
        open={isDeleteServerModalVisible} 
        okText="Да"
        cancelText="Нет"
        onOk={() => 
          {
            deleteServer(remoteServerData?.key ?? -1)}
          } 
        onCancel={() => { 
          setIsDeleteServerModalVisible(false); 
          setRemoteServer(null)
        }}
      > 
        <Paragraph>
          <pre>
            {remoteServerData?.owner && <>Владелец сервера - {remoteServerData.owner}<br/></>}
            Название сервера - {remoteServerData?.name}<br/>
            IP-адрес сервера - {remoteServerData?.ip}<br/> 
            Расположение сервера - {countriesData.find((function(item) {  
              return item.code == remoteServerData?.country  
              }))?.name ?? undefined
            }<br/>
            Статус сервера - {remoteServerData?.status && serverStatusMap[remoteServerData?.status]}  
          </pre>
        </Paragraph>
      </Modal>
      <Modal 
        title="Выберите, кому хотите передать сервер"
        open={isTransferServerModalVisible} 
        okText="Передать"
        cancelText="Не передавать"
        okButtonProps={{ disabled: !serverTransferUserState }}
        onOk={() => 
          {
            transferServer(remoteServerData?.key ?? -1, serverTransferUserState ?? "")}
          } 
        onCancel={() => { 
          setIsTransferServerModalVisible(false); 
          setServerTransferUserState(undefined)
          setRemoteServer(null)
        }}
      > 
        <Paragraph>
          <pre>
            Текущий владелец сервера - {remoteServerData?.owner}<br/>
            Название сервера - {remoteServerData?.name}<br/>
            IP-адрес сервера - {remoteServerData?.ip}<br/> 
            Расположение сервера - {countriesData.find((function(item) {  
              return item.code == remoteServerData?.country  
              }))?.name ?? undefined
            }<br/>
            Статус сервера - {remoteServerData?.status && serverStatusMap[remoteServerData?.status]}  
          </pre>
          <Select
            allowClear
            value={serverTransferUserState}
            style={stylesForSelectField}
            placeholder="Выберите владельца"
            options={usersOptions}
            onChange={(value) => setServerTransferUserState(value)}
          /> 
        </Paragraph>
      </Modal>
    </>
  );
};
