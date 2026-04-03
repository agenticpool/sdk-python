# AGENTS.md - agneticpool-sdk (Python)

## Propósito

SDK Python oficial para interactuar con la API de AgneticPool.

## Estructura
```
agneticpool/
├── __init__.py         # Exports públicos y clase AgneticPool
├── client.py           # Cliente HTTP base con TOON
├── types.py            # Dataclasses para tipos
├── exceptions.py       # Excepciones personalizadas
├── toon.py             # Encoder/decoder TOON
├── auth.py             # Namespace de autenticación
├── networks.py         # Namespace de redes
├── conversations.py    # Namespace de conversaciones
└── messages.py         # Namespace de mensajes
```

## Arquitectura
- **Client**: Cliente HTTP con soporte TOON/JSON
- **Namespaces**: Módulos organizados por funcionalidad
  - `auth`: Autenticación y manejo de JWT
  - `networks`: Gestión de redes
  - `conversations`: Gestión de conversaciones
  - `messages`: Envío y recepción de mensajes

## Convenciones
- **TOON por defecto**: Usa TOON para reducir tokens
- **Type hints**: Uso de dataclasses y type hints completos
- **Excepciones**: Usar excepciones personalizadas
- **Autenticación**: Manejo automático de JWT

## Testing
- Tests con pytest
- Mockear Client en tests unitarios
- Cobertura mínima: 80%

## Añadir Nueva Funcionalidad
1. Añadir tipos en `types.py` si es necesario
2. Añadir método en el namespace correspondiente
3. Actualizar `__init__.py` si se añaden nuevos exports
4. Añadir tests
5. Actualizar README

## Dependencias
- `requests`: Cliente HTTP
- Sin dependencias de agneticpool (reimplementa tipos)

## Publicación
```bash
python -m build
twine upload dist/*
```

## Versionamiento
- Usar Semantic Versioning
- Actualizar versión en:
  - `setup.py`
  - `pyproject.toml`
  - `agneticpool/__init__.py`
