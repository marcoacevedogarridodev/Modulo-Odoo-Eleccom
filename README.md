### Modulo-Odoo-Aeropost

C:\odoo-docker-test\custom-addons\eleccom

Ingresar a instancia aws
-  ssh -i ".\odoo-key.pem" ubuntu@ip publica 

Actualizacion de modulo
- docker-compose run --rm odoo odoo -d postgres -u eleccom --stop-after-init

Subir archivos a aws (recompila el modulo.)
- scp -i "C:\Users\marco\key-aws\odoo-key.pem" -r "C:\odoo-docker-test\custom-addons\eleccom" ubuntu@18.225.10.233:/home/ubuntu/odoo-docker/custom-addons/

recompila las vistas, assets (CSS/JS).
- ubuntu@ip-172-31-41-204:~/odoo-docker$ docker-compose run --rm odoo odoo -d postgres -u eleccom --stop-after-init

Bajar contenedor docker
- docker-compose down

Subir contenedor docker 
- docker-compose up -d

Restart contenedor docker 
- docker-compose restart

Modo debug 
- web?debug=1
