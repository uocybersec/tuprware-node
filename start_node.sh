echo "[!] If any errors occur, make sure you ran the "setup_redis.sh" script.";

python3 build_challenges.py
sudo -u redis redis-server /etc/redis/redis.conf

python3 main.py

