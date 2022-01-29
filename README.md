# aviata_test_v2
1. git clone git@github.com:madein713/aviata_test_v2.git
2. docker-compose up -d --build
3. docker-compose exec airflow bash
4. alembic upgrade head
5. ctrl + D
6. Скопировать localhost:9000/docs и вставить в браузер
7. Добавить провайдеров localhost:9000/api/create-proovider (обязательно url должны быть http://provider_a:9001 и http://provider_b:9002)
8. localhost:9000/search или в сваггере
9. localhost:9000/result/{search_id} или в сваггере
