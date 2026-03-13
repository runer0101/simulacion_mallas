# Plan de mejoras por fases

Este documento organiza las mejoras recomendadas para el proyecto en un roadmap incremental.

## Fase 1 — Estabilización (completada en esta reorganización)

- Limpieza de frontend:
  - Se eliminó código JS no utilizado (exportación CSV y copia de resultados no conectadas a UI).
  - Se eliminó dependencia de `onclick` inline y se reemplazó por binding desde JavaScript.
  - Se consolidó la inicialización `DOMContentLoaded` en un solo bloque.
- Consistencia de validaciones:
  - Rangos de frontend y backend alineados para resistencias y voltajes.
  - Voltajes permitidos desde `0V` para soportar casos de ejemplo con fuentes ausentes.
- Estabilidad de servidor:
  - Matplotlib configurado con backend `Agg` para evitar advertencias de GUI en entorno servidor.
- Dependencias:
  - `requirements.txt` actualizado con rangos compatibles para Python actual.
- Mantenibilidad visual:
  - Se removieron estilos inline críticos y se trasladaron a clases CSS.
  - Se corrigieron selectores de validación que no coincidían con el HTML real.

## Fase 2 — Reestructuración de arquitectura

- Separar `app.py` en módulos:
  - `src/routes/web.py`
  - `src/routes/api.py`
  - `src/services/mesh_analyzer.py`
  - `src/services/circuit_renderer.py`
  - `src/validators/inputs.py`
  - `src/config.py`
- Introducir patrón Application Factory (`create_app`) para facilitar testing y despliegue.
- Centralizar constantes (rangos, mensajes, defaults) en un único módulo.

## Fase 3 — Calidad y pruebas

- Agregar pruebas automatizadas con `pytest`:
  - Validaciones de entrada.
  - Casos de cálculo de mallas.
  - Endpoints `/api/calculate` y `/api/example`.
- Incorporar linting/formato:
  - `ruff` (lint)
  - `black` (formato)
- Añadir flujo de CI (GitHub Actions): tests + lint en cada push/PR.

## Fase 4 — Mejora visual y UX

- Crear sistema de diseño básico (tokens de color, tipografía y espaciado).
- Migrar tamaños críticos de `vw` a `rem` + `clamp()` para mejor legibilidad.
- Mejorar accesibilidad:
  - `:focus-visible`
  - contraste de texto
  - mensajes de error accesibles
- Mejorar visualización de resultados:
  - resumen compacto
  - indicadores por severidad de corriente
  - presentación más limpia en móvil

## Fase 5 — Funcionalidad avanzada

- Exportación real de resultados (CSV/PDF) con botón en UI.
- Historial de simulaciones en memoria o almacenamiento liviano.
- Comparación de escenarios (antes/después) para análisis de optimización.
- Endpoint de reporte técnico con métricas agregadas.

## Fase 6 — Despliegue y operación

- Contenerización con Docker.
- Configuración de producción (WSGI, variables de entorno, logs estructurados).
- Observabilidad básica:
  - healthcheck
  - métricas de uso
  - trazas de errores

---

## Criterio de priorización

1. Estabilidad y consistencia funcional.
2. Mantenibilidad del código.
3. UX y accesibilidad.
4. Funciones avanzadas.
5. Operación en producción.

---

## Actualización de estado (2026-03-05)

- Fase 2 (parcial, completada en esta iteración):
  - `create_app` y separación por módulos ya operativa.
  - Centralización de constantes en `src/config.py`.
  - Validaciones extraídas a `src/validators/inputs.py`.
- Fase 3 (completada en esta iteración):
  - Pruebas con `pytest` para validadores, lógica de mallas y endpoints API.
  - Configuración de `ruff` y `black`.
  - Workflow de CI en GitHub Actions para lint + formato + tests.

## Actualización de estado (2026-03-13)

- Fase 3 (refuerzo):
  - Cobertura ampliada de errores API (415 no JSON, 400 JSON malformado).
  - Cobertura de handlers web 404 y 500.
- Fase 6 (avance operativo):
  - Observabilidad con logs enriquecidos (method, path, query).
  - Endpoints operativos: `GET /api/health` y `GET /api/version`.
