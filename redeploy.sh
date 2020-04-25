docker-compose -f docker-compose.prod.yml pull;
docker-compose -f docker-compose.prod.yml up -d;
docker-compose -f docker-compose.prod.yml exec django python manage.py collectstatic;
docker-compose -f docker-compose.prod.yml exec django python manage.py makemigrations;
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate;
docker-compose -f docker-compose.prod.yml restart django;