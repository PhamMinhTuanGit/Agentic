docker run --name mysql-server \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=chat_history_db \
  -p 3306:3306 \
  -d mysql:8.0 \