# Foodgram
## visit http://localhost:8000/api/schema/redoc/ to check out api endpoints

### Embark on a culinary adventure with Foodgram, a dynamic web application seamlessly blending the power of Django REST API and React. From user-friendly registration to intuitive recipe creation, curated favorites, and efficient shopping list management, Foodgram enriches your cooking experience. With a community-centric approach, connect with fellow food enthusiasts, explore diverse recipes through tag-based filtering, and enjoy the responsive design for a delightful journey into the world of flavors and aromas. Join Foodgram today and turn your kitchen into a canvas of creativity!

## Used technologies:
#### Django
#### Django REST
#### React

## Start the project:

### Clone the repository
```bash
git clone git@github.com:lopentusska/foodgram.git
```

### Create .env file with the following script
```bash
cd foodgram/
echo '''DB_NAME=foodgram_db
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_HOST=localhost
DB_PORT=5432
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1 localhost
REACT_APP_REACT_PROXY=http://localhost:8000/''' > .env
```

# Run project in docker:

## Runs on the localhost:8000

```bash
cd infra
docker compose up -d
```
#### wait some time to let docker build containers

#### logs:
```bash
docker logs <container_name> -f
```

#### stop containers:
```bash
docker compose down
```

# Run locally:
## python3.9 node13.12.0

## Frontend runs on the port 3000
## Backend runs on the port 8000

## Start backend

### postgresql
```bash
sudo su postgres
psql
CREATE DATABASE foodgram_db;
CREATE USER foodgram_user WITH PASSWORD 'foodgram_password';
GRANT ALL PRIVILEGES ON DATABASE foodgram_db TO foodgram_user;
ALTER USER foodgram_user CREATEDB;
```

### Create venv and install requirements.txt
```bash
cd backend/
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Run migrations and start server
```bash
python manage.py migrate
python manage.py load_ingredients
python manage.py load_tags
python manage.py runserver
```

### Optionally create superuser
```bash
python manage.py createsuperuser
```

## Start frontend
```bash
cd frontend/
npm install 
npm start
```
