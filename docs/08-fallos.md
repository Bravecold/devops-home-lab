# 8. Laboratorio de fallos y recuperación

Practica en una ventana controlada. Antes de cada ejercicio registra estado esperado, hipótesis, señal de detección y comando de reversión.

## Método universal

1. **Identificar:** síntoma e impacto.
2. **Delimitar:** componente, usuarios y momento de inicio.
3. **Recolectar:** eventos, logs, métricas y cambios recientes.
4. **Explicar:** causa raíz comprobable, no sólo el error visible.
5. **Corregir:** cambio mínimo y reversible.
6. **Verificar:** funcionalidad y señales durante varios minutos.
7. **Prevenir:** prueba, alerta, automatización o runbook.

## Escenarios

### A. Readiness incorrecta

```bash
kubectl -n devops-lab patch deployment api --type=json \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/readinessProbe/httpGet/path","value":"/does-not-exist"}]'
kubectl -n devops-lab rollout status deployment/api --timeout=60s
kubectl -n devops-lab describe pods
git checkout -- k8s/app.yaml
kubectl apply -f k8s/app.yaml
```

### B. Imagen inexistente

```bash
kubectl -n devops-lab set image deployment/api api=control.lab:5000/devops-lab-api:missing
kubectl -n devops-lab get pods -w
kubectl -n devops-lab describe pods
kubectl -n devops-lab rollout undo deployment/api
```

### C. Service sin endpoints

Cambia temporalmente el selector de `api` y observa `EndpointSlice`, Ingress y logs. Restaura con `kubectl apply -f k8s/app.yaml`.

### D. Presión de recursos

Reduce el límite de memoria por debajo del consumo real, observa `OOMKilled`, `kubectl top pods` y eventos, luego revierte. No ejecutes cargas de estrés fuera del laboratorio.

### E. Base de datos no disponible

Escala PostgreSQL a cero, confirma que liveness continúa pero readiness falla, observa errores y restaura una réplica.

## Plantilla de postmortem

```markdown
# Incidente: título
- Fecha, duración e impacto:
- Detección:
- Línea de tiempo:
- Causa raíz y factores contribuyentes:
- Resolución y evidencia de recuperación:
- Qué funcionó / qué dificultó responder:
- Acciones: responsable, prioridad y fecha:
```

## Criterio de salida

Completa al menos cinco escenarios, recupera el servicio sin reconstrucción manual y publica evidencia anonimizada: comandos, eventos, gráficos y postmortem.

