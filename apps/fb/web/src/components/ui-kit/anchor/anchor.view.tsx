interface AnchorProps {
  href: string
  children: React.ReactNode
}

export function Anchor(props: AnchorProps): React.ReactElement {
  // const bind = useSmoothScrollTo(props.href)
  return <div>{props.children}</div>
}
