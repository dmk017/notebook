import {
  Objects,
  SearchFiltersList,
  SearchObject,
} from '../../store/main-api/generate/api'

export interface ObjectType extends Objects {}
export interface SearchFiltersListWithKey extends SearchFiltersList {
  key: string
}
export interface SearchObjectWithKey extends Omit<SearchObject, 'filters'> {
  filters: SearchFiltersListWithKey[]
}
