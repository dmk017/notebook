import { useRouter } from 'next/router'
import React, { useEffect } from 'react'
import { RootRoutingPath } from '../../../routes'
import _ from 'lodash'

export default function ModelIndexPage() {
  const router = useRouter()
  console.log(router.query)
  const modelId =
    router.query.id instanceof Array
      ? _.first(router.query.id)
      : router.query.id
  useEffect(() => {
    if (modelId) router.push(`${RootRoutingPath.MODELS}/${modelId}/history`)
  }, [modelId, router])
  return <div>Redirect to history...</div>
}
