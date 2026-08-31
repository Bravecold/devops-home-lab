# 3. Docker y Docker Compose

## 1. Instalar Docker en Ubuntu

Usa el repositorio oficial de Docker en un entorno real; el playbook de Ansible instala los paquetes disponibles en Ubuntu para simplificar el laboratorio. Añade tu usuario al grupo sólo si aceptas que equivale prácticamente a privilegios root:

```bash
sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
docker run --rm hello-world
```

## 2. Construir y ejecutar

```bash
docker compose build --pull
docker compose up -d
docker compose ps
curl -fsS http://localhost:8088/ready | jq
docker compose logs --tail=100 api
```

El volumen `postgres_data` sobrevive a una recreación. Compruébalo:

```bash
docker compose exec db psql -U lab -d lab -c 'select now();'
docker compose down
docker compose up -d
```

`docker compose down -v` borra los datos del laboratorio; úsalo sólo cuando quieras reinicializar.

## 3. Inspección y redes

```bash
docker compose config
docker network inspect devops-home-lab_labnet
docker inspect --format '{{json .State.Health}}' devops-api | jq
docker stats --no-stream
```

Los servicios se resuelven por nombre (`db`, `redis`); no fijes IP de contenedor.

## 4. Fallo controlado

```bash
docker compose stop redis
curl -i http://localhost:8088/ready
docker compose logs --since=2m api
docker compose start redis
curl -fsS http://localhost:8088/ready
```

## Criterio de salida

- [ ] Todas las pruebas pasan durante el build.
- [ ] API responde y las dependencias están saludables.
- [ ] Datos persisten tras recrear contenedores.
- [ ] Un fallo de Redis se refleja en readiness y se recupera.

