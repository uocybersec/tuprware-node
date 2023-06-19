echo "[!] If any errors occur, make sure you ran the "setup.sh" script.";

sudo -u redis redis-server /etc/redis/redis.conf

python3 main.py

