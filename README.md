# tracker_cripto
Aplicación Web de Seguimiento de CriptomonedasEsta es una aplicación web construida con Flask que permite a los usuarios suscribirse al seguimiento de precios de criptomonedas, ver variaciones de precios y recibir notificaciones por cambios significativos en un período de 24 horas. Utiliza JWT para autenticación e integra una API externa (por ejemplo, CoinGecko) para obtener precios de criptomonedas en tiempo real.Requisitos PreviosPython 3.8+
Pip (gestor de paquetes de Python)

Instalación1. Clonar el Repositoriobash

git clone https://github.com/tu-usuario/crypto-tracker.git
cd crypto-tracker

2. Instalar DependenciasInstala los paquetes de Python requeridos usando pip:bash

pip install -r requirements.txt

Si requirements.txt no está presente, créalo listando las dependencias:bash

echo "flask\nflask-jwt-extended\nflask-sqlalchemy\npsycopg2-binary\nrequests\npython-dotenv\napscheduler" > requirements.txt

3. Configurar Variables de EntornoCrea un archivo .env en el directorio raíz y agrega las siguientes variables:

SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=tu-clave-jwt-secreta-aqui
DATABASE_URL=sqlite:///crypto_tracker.db  # Usa PostgreSQL si prefieres: postgresql://usuario:contraseña@localhost/nombrebd
COINGECKO_API_KEY=tu-clave-de-coingecko  # Opcional, para la API de CoinGecko si es necesario

Reemplaza tu-clave-secreta-aqui, tu-clave-jwt-secreta-aqui y tu-clave-de-coingecko con valores seguros.
Para producción, usa una base de datos PostgreSQL y protege estas claves.

4. Configurar la Base de DatosInicializa la base de datos ejecutando la aplicación una vez con el siguiente comando, lo que creará las tablas necesarias:bash

python run.py

Esto creará una base de datos SQLite (crypto_tracker.db) por defecto. Si usas PostgreSQL, asegúrate de que la base de datos esté creada y la DATABASE_URL esté correctamente configurada.Ejecutar la AplicaciónInicia la aplicación Flask:

bash

python run.py

La aplicación se ejecutará en modo de depuración en http://127.0.0.1:5000/.
El programador verificará automáticamente los precios de las criptomonedas cada hora y activará notificaciones.

Probar los Endpoints de la API
Usa una herramienta como Postman o curl para interactuar con los siguientes endpoints:

Registrar un usuario (POST /register):json

{
  "username": "usuario1",
  "password": "contraseña123"
}

Iniciar sesión (POST /login):json

{
  "username": "usuario1",
  "password": "contraseña123"
}

Devuelve un token JWT para usar en solicitudes posteriores (inclúyelo en el encabezado Authorization: Bearer <token>).

Suscribirse a una criptomoneda (POST /subscribe/<crypto_id>):Ejemplo: POST /subscribe/bitcoin con un token JWT válido.

Obtener precios y variaciones (GET /prices):Ejemplo: GET /prices con un token JWT válido.

CaracterísticasAutenticación de usuarios mediante JWT.
Suscripción a múltiples criptomonedas (por ejemplo, "bitcoin", "ethereum").
Seguimiento de precios en tiempo real y análisis de variaciones en 24 horas usando la API de CoinGecko.
Notificaciones automáticas para variaciones de precio superiores al 5% (configurable) mediante el programador.

PersonalizaciónSistema de Notificaciones: Actualmente, las notificaciones se imprimen en la consola. Integra correo electrónico (por ejemplo, SendGrid) o SMS (por ejemplo, Twilio) modificando la función check_prices en app/scheduler.py.
Intervalo de Verificación de Precios: Ajusta el intervalo del programador en app/scheduler.py (por defecto es 1 hora).
Umbral de Variación: Modifica la condición abs(variation) > 5 en check_prices para cambiar el desencadenante de notificaciones.

DesarrolloAgregar Frontend: Crea plantillas en app/templates/ o integra un framework de frontend (por ejemplo, React) para una mejor interfaz de usuario.
Seguridad: Hashea las contraseñas usando werkzeug.security y usa variables de entorno de forma segura en producción.
Escalabilidad: Para producción, usa Gunicorn como servidor WSGI y Celery para la programación de tareas.

ContribuyendoSiéntete libre de bifurcar este repositorio, enviar problemas o enviar solicitudes de extracción. Asegúrate de seguir la estructura del proyecto y actualizar el README.md si agregas nuevas características.Licencia[Licencia MIT] - Modifica esta sección con la licencia de tu preferencia.Instrucciones para agregar al proyectoCrea un archivo llamado README.md en la raíz de tu proyecto (crypto-tracker/).
Copia y pega el contenido anterior en ese archivo.
Ajusta las URLs de GitHub (si aplican) y la licencia según tus preferencias.
Si usas Git, confirma los cambios:bash

git add README.md
git commit -m "Agregar README con instrucciones de configuración"
git push

