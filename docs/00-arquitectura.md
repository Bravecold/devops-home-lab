# 0. Arquitectura y preparación

## Objetivo

Definir un laboratorio aislado, repetible y suficientemente pequeño para poder romperlo y reconstruirlo.

## 1. Inventario previo

Comprueba en la estación de trabajo:

```bash
lscpu | sed -n '1,12p'
free -h
df -h /
ip -br address
git --version
ssh -V
```

En macOS usa `sysctl -n hw.ncpu`, `sysctl -n hw.memsize` y `df -h /`. Activa VT-x/AMD-V en BIOS/UEFI si usarás máquinas virtuales.

## 2. Capas del laboratorio

- **Control:** Git, Jenkins, Ansible y registro de imágenes.
- **Aplicación:** K3s, Ingress y workloads.
- **Observabilidad:** Prometheus, Grafana y Loki.
- **Red privada:** tráfico este-oeste; sólo Ingress debe recibir tráfico de usuario.

## 3. Red

Usa una red *host-only* o una VLAN de laboratorio. Mantén NAT únicamente para actualizaciones. Añade en cada nodo:

```text
192.168.56.10 control.lab control
192.168.56.11 worker1.lab worker1
192.168.56.12 worker2.lab worker2
```

Guárdalo en `/etc/hosts`. Verifica resolución directa y conectividad:

```bash
getent hosts control.lab worker1.lab worker2.lab
ping -c 2 worker1.lab
ip route
```

## 4. Puertos previstos

| Puerto | Origen permitido | Uso |
|---:|---|---|
| 22/TCP | red del lab | SSH |
| 80, 443/TCP | estación/red del lab | Ingress |
| 5000/TCP | nodos del lab | registro privado |
| 8080/TCP | estación | Jenkins |
| 3000/TCP | estación | Grafana |
| 9090/TCP | estación | Prometheus |
| 6443/TCP | nodos/control | API de Kubernetes |

No abras PostgreSQL o Redis fuera del clúster.

## 5. Registro de decisiones

Crea una *Architecture Decision Record* por decisión importante: hipervisor, distribución, rango IP, K3s frente a kubeadm, almacenamiento y estrategia de secretos. Formato mínimo: contexto, decisión, alternativas y consecuencias.

## Criterio de salida

- [ ] Recursos medidos y perfil elegido.
- [ ] IP, hostname y función de cada nodo documentados.
- [ ] Red privada aislada y resolución de nombres operativa.
- [ ] Puertos y límites de confianza explícitos.
- [ ] Snapshot/base limpia de cada VM.

