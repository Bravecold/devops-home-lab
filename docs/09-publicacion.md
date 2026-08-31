# 9. Publicar en GitHub y convertir en serie de blog

## Preparar GitHub

1. Ejecuta `git status` y una búsqueda de secretos antes del primer push.
2. Personaliza IP, dominio, usuario y decisiones; no publiques kubeconfig ni inventario real.
3. Añade capturas propias con texto alternativo y elimina hostnames/tokens.
4. Crea un repositorio, configura `origin` y publica `main`.
5. Activa protección de rama, análisis de secretos y Dependabot si aplican.
6. Crea una release `v0.1.0` con requisitos, alcance y limitaciones conocidas.

```bash
git grep -nEi '(password|token|secret|BEGIN .*PRIVATE KEY)' -- ':!docs/*'
git remote add origin git@github.com:TU_USUARIO/devops-home-lab.git
git push -u origin main
```

Revisa manualmente los resultados: algunas coincidencias son nombres de variables; otras pueden ser secretos reales.

## Serie sugerida para el blog

1. La arquitectura y las decisiones.
2. Base Linux, SSH y redes.
3. Una aplicación containerizada con dependencias reales.
4. Configuración reproducible con Ansible.
5. CI y registro de imágenes.
6. Kubernetes: despliegue seguro y rollback.
7. Métricas, dashboards y logs.
8. Cinco fallos, cinco diagnósticos y lo aprendido.

Cada artículo debe incluir: objetivo, diagrama propio, requisitos, pasos, explicación de por qué, validación, fallo habitual, limpieza y enlace al commit/tag exacto. Evita copiar el PDF o sus imágenes; enlázalo como inspiración cuando tengas autorización y usa tus propias capturas.

## Evidencia que aporta valor

- salida reducida de validaciones, no paredes de logs;
- capturas de un pipeline verde y uno fallido;
- dashboard durante un fallo controlado;
- historial de rollout y rollback;
- tabla “síntoma -> evidencia -> causa -> corrección”.

## Checklist editorial

- [ ] Comandos probados desde una instalación limpia.
- [ ] Versiones y fecha visibles.
- [ ] Secretos, IP públicas y datos personales eliminados.
- [ ] Código con lenguaje indicado y líneas razonables.
- [ ] Imágenes propias, comprimidas y con texto alternativo.
- [ ] Limitaciones y costos operativos declarados.
- [ ] Enlaces relativos válidos y licencia incluida.

