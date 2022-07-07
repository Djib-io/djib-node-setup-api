
nohup python3 -u main.py run --username root > ./running.log 2>&1 & echo $! >> root.pid
