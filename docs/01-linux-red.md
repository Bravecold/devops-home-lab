# 1. Linux, SSH y red

Los comandos asumen Ubuntu 22.04/24.04 LTS y un usuario inicial con `sudo`.

## 1. Preparar cada servidor

```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt install -y curl ca-certificates git jq vim ufw chrony
sudo hostnamectl set-hostname worker1   # ajusta en cada nodo
sudo timedatectl set-timezone America/Bogota
sudo systemctl enable --now chrony
```

Crea el usuario de automatización:

```bash
sudo adduser devops
sudo usermod -aG sudo devops
sudo install -d -m 700 -o devops -g devops /home/devops/.ssh
```

## 2. Autenticación por clave

En la estación de control:

```bash
ssh-keygen -t ed25519 -a 64 -f ~/.ssh/devops_lab -C devops-lab
ssh-copy-id -i ~/.ssh/devops_lab.pub devops@worker1.lab
ssh-copy-id -i ~/.ssh/devops_lab.pub devops@worker2.lab
ssh -i ~/.ssh/devops_lab devops@worker1.lab 'hostname && id'
```

Sólo después de verificar una segunda sesión, crea `/etc/ssh/sshd_config.d/10-lab-hardening.conf`:

```text
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
```

Valida antes de reiniciar: `sudo sshd -t && sudo systemctl reload ssh`.

## 3. Firewall

Ejemplo en los workers:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.56.0/24 to any port 22 proto tcp
sudo ufw allow from 192.168.56.0/24 to any port 6443 proto tcp
sudo ufw allow from 192.168.56.0/24 to any port 80 proto tcp
sudo ufw allow from 192.168.56.0/24 to any port 443 proto tcp
sudo ufw enable
sudo ufw status numbered
```

K3s necesita tráfico adicional entre nodos (8472/UDP para Flannel y 10250/TCP para kubelet). Permítelo únicamente desde la subred del laboratorio. Si UFW interfiere con CNI, documenta y limita la excepción; no lo desactives sin registrar el riesgo.

## 4. Diagnóstico de red

```bash
ip -br a
ip route
getent hosts worker2.lab
ss -lntup
curl -v http://worker1.lab
traceroute 8.8.8.8
```

Orden de diagnóstico: interfaz y dirección -> ruta -> resolución DNS -> firewall -> socket en escucha -> aplicación.

## 5. Diagnóstico de servicios

```bash
systemctl status ssh --no-pager
journalctl -u ssh --since '15 minutes ago'
ps aux --sort=-%mem | head
df -h
free -h
```

## Criterio de salida

- [ ] Acceso SSH por clave desde control a ambos workers.
- [ ] Login root y contraseña SSH deshabilitados sin perder acceso.
- [ ] Reloj sincronizado, resolución correcta y firewall documentado.
- [ ] Evidencia guardada de `ss`, `ip route` y una conexión exitosa.

