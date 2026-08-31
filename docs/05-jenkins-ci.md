# 5. Integración continua con Jenkins

## 1. Levantar Jenkins

Para el laboratorio puede ejecutarse en Docker, montando un volumen persistente. El agente que construye imágenes necesita acceso a un daemon Docker; eso otorga privilegios elevados y debe permanecer en la red del lab.

```bash
docker volume create jenkins_home
docker run -d --name jenkins --restart unless-stopped \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts-jdk17
docker logs jenkins
```

Abre `http://control.lab:8080`, completa el asistente e instala Pipeline, Git, Credentials Binding y Docker Pipeline. En una implementación más segura, usa un agente efímero separado para builds.

## 2. Credenciales

Crea en Jenkins:

- `registry-credentials`: usuario/contraseña del registro;
- credencial Git si el repositorio es privado;
- kubeconfig como *Secret file* sólo cuando decidas automatizar despliegues.

Nunca escribas valores secretos en el Jenkinsfile.

## 3. Pipeline

Crea un trabajo *Multibranch Pipeline* apuntando al repositorio. `jenkins/Jenkinsfile` ejecuta pruebas, construye una imagen inmutable, la publica y conserva resultados. Define `REGISTRY=control.lab:5000` y adapta `IMAGE`.

Etiqueta recomendada: `${GIT_COMMIT.take(12)}` y, para releases, el tag semántico. El despliegue debe referenciar ese valor, no `latest`.

## 4. Webhook y calidad

Configura webhook desde GitHub hacia Jenkins sólo mediante túnel/VPN o un endpoint autenticado. Como alternativa segura para un lab privado, usa sondeo periódico. Protege `main` exigiendo el estado del pipeline.

## 5. Diagnóstico

Si falla: identifica la primera etapa roja, revisa su log, reproduce el comando localmente, corrige una causa por vez y vuelve a ejecutar. Archiva JUnit incluso cuando fallen pruebas.

## Criterio de salida

Un commit dispara el pipeline; las pruebas fallidas detienen el build; un commit válido produce una imagen consultable en el registro por tag inmutable.

