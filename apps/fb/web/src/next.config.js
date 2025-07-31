/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['antd'],
  images: {
    domains: ['127.0.0.1', 'localhost'],
    remotePatterns: [
      {
        protocol: 'http',
        hostname: '**',
        port: '',
        pathname: '**',
      },
    ],
  },
  env: {
    BACKEND_URL: process.env.BACKEND_URL,
    ADMIN_API_URL: process.env.ADMIN_API_URL,
    ROOT_GROUP_ID: process.env.ROOT_GROUP_ID,
    LOGOUT_URI: process.env.LOGOUT_URI,
  },
}

module.exports = nextConfig
