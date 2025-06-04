FROM node:20.11-alpine AS build
ENV CYPRESS_INSTALL_BINARY=0
# ARG CONFIG
# ARG BASE_HREF
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm config set strict-ssl false
RUN npm install
COPY . .
# RUN node --max_old_space_size=8000 ./node_modules/@angular/cli/bin/ng build --configuration=${CONFIG} --base-href /${BASE_HREF}/
RUN node --max_old_space_size=8000 ./node_modules/@angular/cli/bin/ng build --configuration=production


FROM nginx:1.18-alpine
# ARG BASE_HREF
COPY nginx.conf /etc/nginx/nginx.conf
# COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html/${BASE_HREF}
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
RUN mkdir /var/cache/nginx/client_temp && \
    mkdir /var/cache/nginx/proxy_temp && \
    mkdir /var/cache/nginx/fastcgi_temp && \
    mkdir /var/cache/nginx/scgi_temp && \
    mkdir /var/cache/nginx/uwsgi_temp && \
    chown -Rf nginx:nginx /var/cache/nginx
USER nginx
CMD ["nginx", "-g", "daemon off;"]
EXPOSE 5000
