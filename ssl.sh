HOST=$1
PUBKEY=$2

certbot -m devs@djuno.io --agree-tos -n --nginx  -d $HOST

sed -i "s~RELAY_PUBLIC_KEY=1~RELAY_PUBLIC_KEY=$PUBKEY~g" /var/djib/relay/.env
sed -i "s~RELAY_DN=~RELAY_DN=$HOST~g" /var/djib/relay/.env

sed -i "s~location / ~ location /test2 ~g" /etc/nginx/sites-available/default

sed -i "s~root /var/www/html;~root /var/www/html; location / {proxy_pass http://localhost:8081;}~g" /etc/nginx/sites-available/default

systemctl reload nginx
systemctl restart djib-relay.service

