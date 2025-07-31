import { Skeleton } from 'antd'
import { useGetObjectApiV1ObjectsIdGetQuery } from '../../../store/main-api/generate/api'
import { ObjectCardView } from './object-card.view'

interface ObjectCardProps {
  objectId: string
}

export function ObjectCard({ objectId }: ObjectCardProps): React.ReactElement {
  const objectState = useGetObjectApiV1ObjectsIdGetQuery({
    id: objectId,
  })

  if (objectState.isLoading || objectState.data == null) {
    return <Skeleton />
  }

  return <ObjectCardView object={objectState.data} />
}
