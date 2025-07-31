import {
  Alert,
  Badge,
  Button,
  DatePicker,
  Divider,
  Flex,
  Form,
  FormInstance,
  Input,
  InputNumber,
  message,
  Modal,
  Space,
  Switch,
  Tabs,
  Tooltip,
  Typography,
  Upload,
  UploadFile,
} from 'antd'
import { AddObjectPayloadType, FileType, ModelType } from '../models.type'
import {
  PropertyPayload,
  ReponseError,
} from '../../../store/main-api/generate/api'
import {
  CheckOutlined,
  CloseOutlined,
  FileAddOutlined,
  InboxOutlined,
  QuestionCircleOutlined,
} from '@ant-design/icons'
import React, { ChangeEvent, useState } from 'react'
import _ from 'lodash'
import { NamePath } from 'antd/es/form/interface'
import { UploadFormField } from './upload-form-field'
import { useResponsive } from '../../../hooks/use-responsive.hook'

const { Title } = Typography

type AddObjectPropertiesPayload = AddObjectPayloadType['properties']

interface ModelCreateFromViewProps {
  model: ModelType
  parseErrors: ReponseError[]

  onSubmit: (values: AddObjectPropertiesPayload) => void

  onSubmitFileUpload: (file: FileType) => void
  isLoadingUploadFile: boolean

  onClickDownlodExampleFileLink: () => void
  isLoadingDownloadFile: boolean
}

interface InputPropertyFormProps {
  form: FormInstance
  modelId: string
  nameField: NamePath
  primitive: PropertyPayload
}

function buildFormFieldName(propertyName: string, primitiveNmae: string) {
  return `${propertyName}-${primitiveNmae}`
}

function InputPropertyForm(props: InputPropertyFormProps): React.ReactElement {
  const { primitive, form, nameField, modelId } = props

  function onChangeField(value: string | boolean | number | UploadFile | null) {
    form.setFieldValue(nameField, value)
  }

  function onBlurField() {
    form.validateFields([nameField])
  }

  switch (primitive.primitive_type) {
    case 'STR':
      return (
        <Input
          placeholder={primitive.help_text ?? undefined}
          onChange={(e: ChangeEvent<HTMLInputElement>) => {
            onChangeField(e.target.value)
          }}
          onBlur={onBlurField}
        />
      )
    case 'BOOL':
      return (
        <Switch
          checkedChildren={<CheckOutlined />}
          unCheckedChildren={<CloseOutlined />}
          onChange={(value) => onChangeField(value)}
        />
      )
    case 'NUMBER':
      return <InputNumber onChange={onChangeField} onBlur={onBlurField} />
    case 'DATE':
      return <DatePicker onChange={onChangeField} />
    case 'FILE':
      return (
        <UploadFormField onSuccesUpload={onChangeField} modelId={modelId} />
      )
    default:
      break
  }
  return <></>
}

export function ModelCreateFromView(
  props: ModelCreateFromViewProps
): React.ReactElement {
  const {
    model,
    parseErrors,
    onSubmit,
    onSubmitFileUpload,
    isLoadingUploadFile,
    onClickDownlodExampleFileLink,
    isLoadingDownloadFile,
  } = props
  const [showModal, setShowModal] = useState<boolean>(false)
  const [tabNumber, setTabNumber] = useState(0)
  const [fileList, setFileList] = useState<UploadFile[]>([])
  const [errors, setErrors] = React.useState([])
  const { isMobile } = useResponsive()

  const [form] = Form.useForm()
  const values = Form.useWatch([], form)

  React.useEffect(() => {
    form.validateFields({ validateOnly: true }).then(
      () => {
        setErrors([])
      },
      (e) => {
        console.log(e)
        setErrors(e.errorFields)
      }
    )
  }, [form, values])

  const submittable = _.isEmpty(errors)

  const handleFinish = (values: AddObjectPropertiesPayload): void => {
    onSubmit(values)
  }

  const acceptFileTypes = [
    'application/vnd.ms-excel',
    // 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheets',
  ]

  return (
    <div>
      <Flex
        align={isMobile ? 'flex-start' : 'center'}
        justify="space-between"
        vertical={isMobile}
      >
        <div>
          <Title level={2}>Создание объекта модели - {model.name}</Title>
        </div>
        <div>
          <Button
            type="primary"
            icon={<FileAddOutlined />}
            onClick={() => setShowModal(true)}
          >
            Загрузка из файла
          </Button>
        </div>
      </Flex>
      <Divider dashed></Divider>
      <Form
        form={form}
        onFinish={handleFinish}
        labelAlign="left"
        validateTrigger="onBlur"
      >
        <Tabs
          activeKey={tabNumber.toString()}
          items={model.properties.map((property, index) => ({
            key: index.toString(),
            label: property.payload.name,
            disabled: tabNumber != index,
            children: (
              <React.Fragment key={index}>
                <Title level={3}>
                  <Badge dot={property.is_required}>
                    Форма ввода: {property.payload.name}
                  </Badge>
                </Title>
                {property.payload.properties.map((primitive, index) => {
                  if (primitive.is_multiple) {
                    return (
                      <Form.Item
                        key={index}
                        label={
                          <Space>
                            <Typography.Text>{primitive.name}</Typography.Text>
                            {primitive.help_text == null ? null : (
                              <Tooltip title={primitive.help_text}>
                                <Button
                                  type="link"
                                  icon={<QuestionCircleOutlined />}
                                />
                              </Tooltip>
                            )}
                          </Space>
                        }
                      >
                        <Form.List
                          name={buildFormFieldName(
                            property.payload.name,
                            primitive.name
                          )}
                          rules={[
                            {
                              validator: async (_, fields) => {
                                if (!fields) {
                                  return Promise.reject(
                                    new Error('Добавьте поле!')
                                  )
                                }
                              },
                            },
                          ]}
                        >
                          {(fields, opt) => (
                            <div
                              style={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: 'flex-start',
                                rowGap: 16,
                              }}
                            >
                              {fields.map((field) => (
                                <Space key={field.key}>
                                  <Form.Item noStyle name={[field.name]}>
                                    <InputPropertyForm
                                      nameField={[
                                        buildFormFieldName(
                                          property.payload.name,
                                          primitive.name
                                        ),
                                        field.name,
                                      ]}
                                      modelId={model._id ?? ''}
                                      primitive={primitive}
                                      form={form}
                                    />
                                  </Form.Item>
                                  <CloseOutlined
                                    onClick={() => {
                                      opt.remove(field.name)
                                    }}
                                  />
                                </Space>
                              ))}
                              <div>
                                <Button type="dashed" onClick={() => opt.add()}>
                                  + элемент
                                </Button>
                              </div>
                            </div>
                          )}
                        </Form.List>
                      </Form.Item>
                    )
                  }

                  return (
                    <Form.Item
                      name={buildFormFieldName(
                        property.payload.name,
                        primitive.name
                      )}
                      label={
                        <Space>
                          <Typography.Text>{primitive.name}</Typography.Text>
                          {primitive.help_text == null ? null : (
                            <Tooltip title={primitive.help_text}>
                              <Button
                                type="link"
                                icon={<QuestionCircleOutlined />}
                              />
                            </Tooltip>
                          )}
                        </Space>
                      }
                      required={primitive.is_required}
                      key={index}
                      rules={[
                        {
                          required: primitive.is_required,
                          message: 'Это поле обязательное',
                        },
                        {
                          pattern: new RegExp(
                            primitive.validation || '^.{2,}$'
                          ),
                          message: 'Поле должно соответствовать валидации',
                        },
                      ]}
                    >
                      <InputPropertyForm
                        nameField={buildFormFieldName(
                          property.payload.name,
                          primitive.name
                        )}
                        modelId={model._id ?? ''}
                        primitive={primitive}
                        form={form}
                      />
                    </Form.Item>
                  )
                })}
              </React.Fragment>
            ),
          }))}
        />
        <Space align="start">
          {tabNumber > 0 ? (
            <Button
              type="dashed"
              onClick={() => setTabNumber((value) => value - 1)}
            >
              Назад
            </Button>
          ) : null}
          {tabNumber < _.size(model.properties) - 1 ? (
            <Button
              type="dashed"
              onClick={() => {
                form
                  .validateFields()
                  .then(() => {
                    setTabNumber((value) => value + 1)
                  })
                  .catch(() => {})
              }}
              disabled={!submittable}
            >
              Далее
            </Button>
          ) : null}
          {tabNumber == _.size(model.properties) - 1 ? (
            <Form.Item>
              <Button type="primary" htmlType="submit" disabled={!submittable}>
                Создать
              </Button>
            </Form.Item>
          ) : null}
        </Space>
      </Form>
      <Modal
        title="Загрузка из файла"
        open={showModal}
        okButtonProps={{ style: { display: 'none' } }}
        cancelButtonProps={{ style: { display: 'none' } }}
        onCancel={() => setShowModal(false)}
        width={isMobile ? undefined : 1000}
      >
        <div>
          <p>Для загрузки объекта требуется заполнить xlsx файл по шаблону</p>
          <p>
            <Button
              type="link"
              onClick={onClickDownlodExampleFileLink}
              loading={isLoadingDownloadFile}
              disabled={isLoadingDownloadFile}
            >
              Скачать шаблон
            </Button>
          </p>
        </div>
        <div>
          <Typography.Title level={5}>
            После заполнения прикрепите в форму ниже
          </Typography.Title>
          <div>
            <Upload.Dragger
              name="file"
              multiple={false}
              maxCount={1}
              accept={acceptFileTypes.join(', ')}
              beforeUpload={(file) => {
                const isXLSX = _.includes(acceptFileTypes, file.type)
                if (!isXLSX) {
                  message.error(`${file.name} - не допустимый формат файла`)
                }
                setFileList((prev) => [...prev, file])
                return isXLSX || Upload.LIST_IGNORE
              }}
            >
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">
                Перетащите или выберите файл для загрузки
              </p>
            </Upload.Dragger>
            <Flex
              align="center"
              justify="space-between"
              style={{ marginTop: 16 }}
            >
              <Button
                type="primary"
                onClick={() => {
                  if (!_.isEmpty(fileList)) {
                    onSubmitFileUpload(_.first(fileList) as FileType) // always exist
                  }
                }}
                loading={isLoadingUploadFile}
                disabled={_.isEmpty(fileList) || isLoadingUploadFile}
              >
                Отправить
              </Button>
              <Button
                onClick={() => {
                  setFileList([])
                  setShowModal(false)
                }}
              >
                Отмена
              </Button>
            </Flex>
          </div>
        </div>
        {parseErrors.length > 0 ? (
          <Alert
            message="Ошибка парсинга файла"
            description={parseErrors.map((error, index) => (
              <div key={index}>
                {`${index + 1}. ${error.details} //`}
                <Typography.Text code>{error.code.message}</Typography.Text>
              </div>
            ))}
            type="warning"
            showIcon
            style={{
              marginTop: 16,
            }}
          />
        ) : null}
      </Modal>
    </div>
  )
}
