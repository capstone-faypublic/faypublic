letsencrypt renew
cp -rL /etc/letsencrypt/live/login.faypublic.tv/* /etc/letsencrypt/copy
docker-compose down
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d