docker-compose down
letsencrypt renew
cp -rL /etc/letsencrypt/live/login.faypublic.tv/* /etc/letsencrypt/copy
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d