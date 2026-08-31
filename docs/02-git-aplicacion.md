# 2. Git y aplicación de ejemplo

## Flujo de trabajo

Protege `main`, crea cambios en `feat/*` o `fix/*`, abre Pull Request y exige pruebas antes de mezclar. Etiqueta entregas como `v0.1.0`.

```bash
git init
git switch -c main
git add .
git commit -m "chore: bootstrap DevOps home lab"
git switch -c feat/health-api
```

## Ejecutar la API sin contenedores

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r app/requirements.txt
pytest app/test_app.py -q
python app/app.py
curl -fsS http://localhost:5000/health | jq
```

Endpoints:

- `/`: identifica la versión y aumenta un contador en Redis.
- `/health`: confirma que el proceso vive.
- `/ready`: comprueba PostgreSQL y Redis; devuelve 503 si una dependencia falla.
- `/metrics`: métricas Prometheus.

## Checklist de Pull Request

- [ ] Cambio pequeño y propósito claro.
- [ ] Pruebas nuevas o actualizadas.
- [ ] Sin secretos ni artefactos generados.
- [ ] Documentación actualizada.
- [ ] Pipeline verde y revisión aprobada.

## Criterio de salida

Pruebas locales verdes, rama publicada, PR revisada y etiqueta `v0.1.0` creada después del merge.

