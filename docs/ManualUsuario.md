# Manual de Usuario - SmartBot

**Autor:** Pablo Alejandro Marroquin Cutz

---

## 1. Requisitos Previos

Antes de ejecutar el proyecto asegurate de tener instalado lo siguiente:

| Herramienta | Version minima | Descarga |
|-------------|---------------|---------|
| Docker Desktop | 4.x | https://www.docker.com/products/docker-desktop |
| Git | 2.x | https://git-scm.com |
| Telegram | Cualquier version | https://telegram.org |

---

## 2. Instalacion y Ejecucion

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/PabloMarroquinnn1/telegram-faq-bot.git
cd telegram-faq-bot
```

### Paso 2 — Configurar el archivo .env

Edita el archivo `.env` en la raiz de `Practica2/` y reemplaza el valor del token:

```env
TELEGRAM_TOKEN=<tu_token_de_botfather>
```

Los demas valores ya estan configurados por defecto y no requieren modificacion.

### Paso 3 — Levantar el proyecto

```bash
docker-compose up --build
```

Espera hasta ver los siguientes mensajes en la terminal:

```
Admin creado
Categorias creadas
20 preguntas cargadas
Config inicial creada
Bot iniciado...
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Paso 4 — Acceder al panel administrativo

Abre tu navegador e ingresa a:

```
http://localhost:8000
```

### Paso 5 — Detener el proyecto

```bash
docker-compose down
```

---

## 3. Uso del Panel Administrativo

### 3.1 Inicio de Sesion

Ingresa las credenciales preconfiguradas del sistema:

| Campo | Valor |
|-------|-------|
| Usuario | `IA1-User` |
| Contrasena | `IA1-password@_new` |

### 3.2 Gestion de Preguntas

En la pestana **Preguntas** puedes realizar las siguientes operaciones:

**Agregar una pregunta:**
1. Escribe el texto de la pregunta en el campo correspondiente
2. Selecciona una categoria del listado
3. Escribe la respuesta en el area de texto
4. Presiona el boton **Guardar**

**Editar una pregunta:**
1. Presiona el boton **Editar** en la fila de la pregunta que deseas modificar
2. El formulario se llenara automaticamente con los datos actuales
3. Modifica los campos que necesites
4. Presiona **Actualizar** para guardar los cambios
5. Presiona **Cancelar** si deseas descartar la edicion

**Eliminar una pregunta:**
1. Presiona el boton **Eliminar** en la fila correspondiente
2. Confirma la accion en el dialogo de confirmacion

> Nota: No se permite registrar dos preguntas con el mismo texto. El sistema mostrara un aviso si intentas crear una pregunta duplicada.

### 3.3 Gestion de Categorias

En la pestana **Categorias** puedes:

**Agregar una categoria:**
1. Escribe el nombre de la nueva categoria
2. Escribe una descripcion opcional
3. Presiona **Guardar**

**Eliminar una categoria:**
1. Presiona el boton **Eliminar** en la fila correspondiente
2. Confirma la accion

Las categorias predefinidas del sistema son: General, Academico y Tecnico.

### 3.4 Estadisticas

En la pestana **Estadisticas** puedes visualizar:

- Total de consultas realizadas al bot
- Cantidad de preguntas registradas en el sistema
- Numero de categorias activas
- Las cinco consultas mas frecuentes de los usuarios
- Historial completo de las ultimas 20 consultas con usuario, fecha y respuesta

### 3.5 Configuracion

En la pestana **Configuracion** puedes ingresar el ID del grupo o chat de Telegram al que el bot enviara mensajes. Ingresa el ID y presiona **Guardar Configuracion**.

---

## 4. Uso del Bot de Telegram

### Encontrar el bot

Para encontrar el bot en Telegram busca el siguiente nombre de usuario en el buscador de la aplicacion:

```
@smartbot_ia1_bot
```

Puedes buscarlo directamente desde la barra de busqueda de Telegram escribiendo `smartbot_ia1_bot`. Una vez que lo encuentres presiona **Iniciar** o **Start** para comenzar.

### Comandos disponibles

| Comando | Descripcion |
|---------|-------------|
| `/start` | Inicia el bot y muestra el mensaje de bienvenida |
| `/help` | Muestra las instrucciones de uso |
| `/categorias` | Lista las categorias de preguntas disponibles |

### Realizar consultas

Escribe tu pregunta directamente en el chat sin necesidad de usar comandos especiales. El bot buscara la respuesta mas adecuada en la base de datos y respondera automaticamente.

Ejemplos de consultas:

```
Que es SmartBot
Como me inscribo a un curso
Cual es la nota minima para aprobar
Como recupero mi contrasena
```

Si el bot no encuentra una respuesta registrada para tu consulta, respondera con un mensaje indicando que no se encontro informacion y sugerira reformular la pregunta o contactar a soporte.

---

## 5. Preguntas Frecuentes Disponibles

El sistema viene precargado con 20 preguntas distribuidas en 3 categorias:

### General
- Que es SmartBot
- Como funciona el bot
- Cual es el horario de atencion
- Como contacto a un humano
- El bot guarda mis mensajes
- Puedo usar el bot desde cualquier dispositivo
- El servicio es gratuito

### Academico
- Como me inscribo a un curso
- Cuando son los periodos de inscripcion
- Como solicito una constancia de estudios
- Como reviso mis notas
- Que hago si repruebo un curso
- Como solicito una revision de examen
- Cual es el minimo de nota para aprobar

### Tecnico
- Como recupero mi contrasena
- Que navegadores son compatibles
- Como accedo al correo institucional
- Que hago si el portal no carga
- Como instalo el software requerido
- Como reporto un problema tecnico

---

## 6. Solucion de Problemas

| Problema | Solucion |
|----------|---------|
| El panel no carga en el navegador | Verifica que Docker este corriendo y ejecuta `docker-compose up` |
| El bot no responde en Telegram | Verifica que el token en el archivo `.env` sea correcto y que el contenedor del bot este activo |
| Error de credenciales al iniciar sesion | Usa exactamente `IA1-User` como usuario y `IA1-password@_new` como contrasena |
| Los contenedores no inician correctamente | Ejecuta `docker-compose down -v` para limpiar volumenes y luego `docker-compose up --build` |
| Mensaje de pregunta duplicada | El sistema no permite registrar dos preguntas con el mismo texto. Modifica el texto de la nueva pregunta |