# Foodgram

## Start the project:

### Clone the repository
```bash
git clone https://github.com/lopentus/foodgram-project-react
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
