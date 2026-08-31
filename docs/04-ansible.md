# 4. Configuración con Ansible

## 1. Preparar inventario

Copia `ansible/inventory.ini.example` a `ansible/inventory.ini` y ajusta IP/usuario. El archivo real está ignorado porque puede revelar infraestructura.

```bash
python3 -m venv .venv-ansible
. .venv-ansible/bin/activate
pip install ansible
ansible all -i ansible/inventory.ini -m ping
```

## 2. Aplicar configuración

```bash
ansible-playbook -i ansible/inventory.ini ansible/playbooks/site.yml --check --diff
ansible-playbook -i ansible/inventory.ini ansible/playbooks/site.yml
ansible-playbook -i ansible/inventory.ini ansible/playbooks/site.yml
```

La segunda ejecución real debe terminar sin cambios relevantes: esa es la prueba de idempotencia.

## 3. Validar

```bash
ansible all -i ansible/inventory.ini -a 'docker --version'
ansible all -i ansible/inventory.ini -a 'systemctl is-active docker'
ansible all -i ansible/inventory.ini -a 'ufw status'
```

Para secretos usa Ansible Vault: `ansible-vault create ansible/group_vars/all/vault.yml`; confirma sólo el archivo cifrado y nunca la contraseña.

## Criterio de salida

Todos los hosts responden, Docker está activo y una segunda ejecución queda idempotente.

