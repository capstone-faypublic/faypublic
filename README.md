# faypublic
User registration, production management, and class scheduling rolled into a happy Django app

## About the project

`faypublic` is an application created by University of Arkansas students for the Fayetteville Public Television organization. 

## Run the project

1. Install [Docker](https://docs.docker.com/engine/installation/).
   On older versions of Windows and versions not Pro or Enterprise install [Docker Toolbox](https://docs.docker.com/toolbox/overview/)
2. Clone the repository and `cd /path/to/faypublic`
3. Rename `.env.example` to `.env`
4. Run the following commands
```bash
docker-compose up
```
5. In a new terminal window, run
```bash
docker-compose restart django # might or might not need this one; wait about 20-30 seconds for postres to start before running it
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate
docker-compose restart django
docker-compose restart celery
```
6. Visit [`http://localhost:8000`](http://localhost:8000)

### Other runtime options

Run the project in the background (detatched): `docker-compose up -d`

Stop all running containers: `docker-compose down`

Execute a command inside of a container (container must be running): `docker-compose exec <container-name> <command>`

Loading seed data (fixtures): `docker-compose exec django python manage.py loaddata`

Export data to fixtures: `docker-compose exec django python manage.py dumpdata`

Create a superuser (admin user): `docker-compose exec django python manage.py createsuperuser`

## Team members
* Garrett Graham [gwadegraham](https://github.com/gwadegraham)
* Ryan Hutslar [rchutsla](https://github.com/rchutsla)
* Jacob Krusz [jkrusz](https://github.com/jkrusz)
* Teja Nakka [tnakka214](https://github.com/tnakka214)
* Blake Reed [BlakeReed19](https://github.com/BlakeReed19)
* Jan Timpe [jan-timpe](https://github.com/jan-timpe)
