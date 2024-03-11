FROM node:18-alpine AS builder

WORKDIR /app

COPY /frontend/package.json ./

RUN npm install

COPY /frontend .

EXPOSE 3000

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/node_modules /app/node_modules

CMD ["npm", "run", "dev"]