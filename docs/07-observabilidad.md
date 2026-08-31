# 7. Métricas, dashboards y logs

## 1. Prometheus y Grafana local

El perfil `monitoring` de Compose levanta Prometheus y Grafana:

```bash
docker compose --profile monitoring up -d
curl -fsS http://localhost:9090/-/ready
curl -fsS http://localhost:3000/api/health
```

Abre Grafana en `http://localhost:3000`, cambia la contraseña inicial y confirma el datasource aprovisionado.

Consultas iniciales:

```promql
rate(http_requests_total[5m])
sum by (status) (rate(http_requests_total[5m]))
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
up
```

Construye un dashboard con tasa de solicitudes, errores, p95, disponibilidad y recursos. Un panel sin unidad, leyenda o horizonte temporal claro no está terminado.

## 2. Prometheus en Kubernetes

Para el clúster, instala `kube-prometheus-stack` con Helm en un namespace `monitoring`; fija una versión del chart y conserva tus `values.yaml`. Activa persistencia sólo si tienes una StorageClass apropiada. No publiques Grafana sin autenticación.

## 3. Logging centralizado

Instala Loki y un recolector compatible (Grafana Alloy o Promtail en laboratorios heredados). Etiquetas recomendadas: namespace, app, container y nivel. Evita etiquetas de alta cardinalidad como request ID o usuario; esos valores deben ir en el cuerpo JSON.

Formato de log recomendado:

```json
{"timestamp":"2026-08-31T12:00:00Z","level":"INFO","service":"api","message":"request complete","status":200,"duration_ms":12}
```

Correlaciona una anomalía: detecta el pico en Prometheus, anota hora/servicio, filtra logs en el mismo intervalo, identifica el primer error y valida recuperación en métricas.

## 4. Alertas

Crea alertas por síntomas: tasa de 5xx, latencia, indisponibilidad y saturación. Cada alerta necesita severidad, duración, descripción y enlace a runbook. Prueba una alerta antes de confiar en ella.

## Criterio de salida

- [ ] Prometheus consulta la API y muestra `up=1`.
- [ ] Dashboard responde disponibilidad, tráfico, errores y latencia.
- [ ] Logs se filtran por aplicación y tiempo.
- [ ] Una alerta de prueba dispara y se resuelve.

