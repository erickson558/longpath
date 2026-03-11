# LongPath Popup Tester

Aplicacion de prueba para validar el escenario de rutas extremadamente largas en un popup, asegurando que:

- Los filepaths largos hagan salto de linea.
- No aparezca scroll horizontal por textos sin corte.

Version actual: consultar `VERSION` (fuente unica de verdad).

## Funcionalidad

- Muestra una ventana principal con boton para abrir un popup de import.
- Permite configurar cuantas rutas generar (por defecto `39090`).
- Genera rutas y archivos reales dentro de `generated_long_paths/` en la misma carpeta de `app.py`.
- El popup renderiza esas rutas profundas en un control con `wrap=tk.WORD`.
- Esto simula el caso reportado en UI para validar que no exista desplazamiento lateral.

## Estructura

- `app.py`: App de escritorio en Tkinter.
- `VERSION`: Version unica del proyecto en formato `Vx.x.x`.
- `build.ps1`: Compilacion a `.exe` en la misma carpeta del proyecto usando `app.ico` local.
- `.github/workflows/release.yml`: Build y release automatico por push a `main`.

## Requisitos

- Python 3.12+
- Windows PowerShell

## Instalacion local

```powershell
python -m pip install -r requirements.txt
```

## Ejecucion local

```powershell
python app.py
```

## Compilacion a EXE

1. Asegura que `app.ico` exista en la misma carpeta que `app.py`.
2. Ejecuta:

```powershell
./build.ps1
```

Resultado: `app.exe` en la raiz del proyecto (misma carpeta que `app.py`).

## Versionado (mejores practicas)

Se usa Semantic Versioning con prefijo `V`:

- `VMAJOR.MINOR.PATCH`
- `MAJOR`: cambios incompatibles.
- `MINOR`: nuevas funcionalidades compatibles.
- `PATCH`: correcciones o ajustes internos.

Regla del repositorio:

- Cada commit a `main` debe incrementar `VERSION`.
- El workflow crea tag/release con ese mismo valor.
- La app muestra exactamente esa misma version en UI.

## Flujo recomendado por commit

1. Cambiar `VERSION` (por ejemplo `V1.0.2`).
2. Actualizar `CHANGELOG.md`.
3. Commit a `main`.
4. GitHub Actions valida y publica release.

## Licencia

Este proyecto esta bajo licencia Apache License 2.0. Ver `LICENSE`.
