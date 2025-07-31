import { useMediaQuery } from 'react-responsive'

interface ResponsiveResponse {
  isDesktop: boolean
  isMobile: boolean
}

const MAX_MOBILE_WIDTH = 1100

export function useResponsive(): ResponsiveResponse {
  return {
    isDesktop: useMediaQuery({ query: `(min-width: ${MAX_MOBILE_WIDTH}px)` }),
    isMobile: useMediaQuery({ query: `(max-width: ${MAX_MOBILE_WIDTH}px)` }),
  }
}
