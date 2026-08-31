# 6. Kubernetes: K3s, despliegue e Ingress

## 1. Crear el clúster

En `worker1`:

```bash
curl -sfL https://get.k3s.io | sh -s - server --write-kubeconfig-mode 640
sudo cat /var/lib/rancher/k3s/server/node-token
sudo kubectl get nodes -o wide
```

En `worker2`, usando el token obtenido de forma segura:

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://worker1.lab:6443 K3S_TOKEN='<TOKEN>' sh -
```

Copia `/etc/rancher/k3s/k3s.yaml` a la estación, cambia `127.0.0.1` por `worker1.lab`, protege el archivo con modo `600` y no lo confirmes en Git.

## 2. Publicar la imagen

Levanta un registro privado con autenticación y TLS para un laboratorio duradero. Para un primer recorrido aislado puedes usar `registry:2` en `control.lab:5000`, pero documenta que HTTP/insecure registry no es aceptable fuera del lab. Configura cada nodo de K3s en `/etc/rancher/k3s/registries.yaml`.

```bash
docker tag devops-lab-api:local control.lab:5000/devops-lab-api:v0.1.0
docker push control.lab:5000/devops-lab-api:v0.1.0
```

Actualiza la imagen en `k8s/app.yaml`.

## 3. Desplegar

```bash
kubectl apply -f k8s/namespace.yaml
kubectl -n devops-lab create secret generic app-secrets \
  --from-literal=POSTGRES_PASSWORD="$(openssl rand -base64 24)" \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f k8s/data.yaml
kubectl apply -f k8s/app.yaml
kubectl apply -f k8s/ingress.yaml
kubectl -n devops-lab rollout status deployment/api --timeout=180s
```

El manifiesto incluye probes, requests/limits, ConfigMap y actualización gradual. PostgreSQL usa almacenamiento local: adecuado para aprender, no para alta disponibilidad.

## 4. Verificar

```bash
kubectl -n devops-lab get all,ingress,pvc
kubectl -n devops-lab get events --sort-by=.lastTimestamp
curl -H 'Host: lab.local' http://worker1.lab/ready
```

Añade `192.168.56.11 lab.local` a `/etc/hosts` si no tienes DNS local.

## 5. Actualizar y revertir

```bash
kubectl -n devops-lab set image deployment/api api=control.lab:5000/devops-lab-api:v0.2.0
kubectl -n devops-lab rollout status deployment/api
kubectl -n devops-lab rollout history deployment/api
kubectl -n devops-lab rollout undo deployment/api
```

## Diagnóstico

```bash
kubectl -n devops-lab get pods -o wide
kubectl -n devops-lab describe pod POD
kubectl -n devops-lab logs POD --all-containers --previous
kubectl -n devops-lab get endpointslices
kubectl -n devops-lab run netcheck --rm -it --image=curlimages/curl -- sh
```

Secuencia: estado/eventos -> logs -> configuración -> Service/EndpointSlice -> DNS/red -> recursos del nodo.

## Criterio de salida

Dos nodos Ready, rollout completo, Ingress funcional, readiness sensible a dependencias y rollback probado.

