# Foodgram
https://github.com/lopentus/foodgram-project-react

### Create .env file with the following script
```bash
cd postgram/
echo '''DB_NAME=foodgram_db
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_HOST=localhost
DB_PORT=5432
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1 localhost
```

#### setup dev
create env
source venv/bin/activate 
cd backend/
pip install -r requirements.txt

### launch the project
python manage.py migrate
python manage.py load_ingredients
python manage.py runserver

#### setup docker
cd foodgram-project-react/infra/
sudo docker compose -f docker-compose.yml up -d
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.yml exec backend python manage.py load_ingredients
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend cp -r /app/static/. /var/html/

CREATE DATABASE foodgram_db;
CREATE USER foodgram_user WITH PASSWORD 'foodgram_password';
GRANT ALL PRIVILEGES ON DATABASE foodgram_db TO foodgram_user;
ALTER USER foodgram_user CREATEDB;

python manage.py migrate

npm install
npm start
