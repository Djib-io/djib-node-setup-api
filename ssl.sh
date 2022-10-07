HOST=$1
PUBKEY=$2

certbot --nginx  -d $HOST

sed -i "s~RELAY_PUBLIC_KEY=1~RELAY_PUBLIC_KEY=$PUBKEY~g" /var/djib/relay/.env
sed -i "s~RELAY_DN=~RELAY_DN=$HOST~g" /var/djib/relay/.env

systemctl restart djib-relay.service

