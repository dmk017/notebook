import { useRouter } from 'next/router'
import React, { useEffect } from 'react'
import { RootRoutingPath } from '../../../routes'
import _ from 'lodash'

export default function PropertyIndexPage() {
  const router = useRouter()
  const propertyId =
    router.query.id instanceof Array
      ? _.first(router.query.id)
      : router.query.id
  useEffect(() => {
    if (propertyId)
      router.push(`${RootRoutingPath.PROPERTIES}/${propertyId}/history`)
  }, [propertyId, router])
  return <div>Redirect to history...</div>
}
