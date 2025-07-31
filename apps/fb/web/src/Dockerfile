FROM node:current-alpine3.16 as base
RUN mkdir /app
WORKDIR /app
COPY package*.json ./
COPY yarn.lock ./
COPY next.config.js ./

FROM base as pre-prod
COPY . .
RUN yarn install --frozen-lockfile
RUN yarn build

FROM node:current-alpine3.16 as prod
RUN mkdir /app
WORKDIR /app
COPY --from=pre-prod /app/public ./public
COPY --from=pre-prod /app/.next ./.next
COPY --from=pre-prod /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node_modules/.bin/next", "start"]