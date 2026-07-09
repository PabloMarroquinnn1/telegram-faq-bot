from app.database import SessionLocal
from app.models.models import AdminUser, Category, Question, BotConfig
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_data():
    db = SessionLocal()
    try:
        # --- Admin user ---
        admin = db.query(AdminUser).filter(AdminUser.username == "IA1-User").first()
        if not admin:
            admin = AdminUser(
                username="IA1-User",
                hashed_password=pwd_context.hash("IA1-password@_new"[:72])
            )
            db.add(admin)
            db.commit()
            print("✅ Admin creado")

        # --- Categorías ---
        categorias = [
            {"name": "General", "description": "Preguntas generales del sistema"},
            {"name": "Académico", "description": "Preguntas sobre trámites académicos"},
            {"name": "Técnico", "description": "Preguntas sobre soporte técnico"},
        ]
        cat_ids = {}
        for c in categorias:
            existing = db.query(Category).filter(Category.name == c["name"]).first()
            if not existing:
                cat = Category(**c)
                db.add(cat)
                db.commit()
                db.refresh(cat)
                cat_ids[c["name"]] = cat.id
            else:
                cat_ids[c["name"]] = existing.id
        print("✅ Categorías creadas")

        # --- Preguntas ---
        if db.query(Question).count() == 0:
            preguntas = [
                # General
                ("¿Qué es SmartBot?", "SmartBot es un sistema automatizado de respuestas basado en Telegram.", "General"),
                ("¿Cómo funciona el bot?", "El bot recibe tus mensajes y busca la respuesta más adecuada en la base de datos.", "General"),
                ("¿Cuál es el horario de atención?", "El bot está disponible las 24 horas del día, los 7 días de la semana.", "General"),
                ("¿Cómo contacto a un humano?", "Puedes escribir al correo soporte@usac.edu.gt para atención personalizada.", "General"),
                ("¿El bot guarda mis mensajes?", "Sí, se registran las consultas para mejorar el servicio.", "General"),
                ("¿Puedo usar el bot desde cualquier dispositivo?", "Sí, puedes acceder desde cualquier dispositivo con Telegram instalado.", "General"),
                ("¿El servicio es gratuito?", "Sí, el uso del bot es completamente gratuito.", "General"),
                # Académico
                ("¿Cómo me inscribo a un curso?", "Debes ingresar al portal estudiantil y seleccionar los cursos disponibles en tu pensum.", "Académico"),
                ("¿Cuándo son los periodos de inscripción?", "Los periodos de inscripción se publican en el portal oficial de la USAC.", "Académico"),
                ("¿Cómo solicito una constancia de estudios?", "Debes ingresar a la ventanilla virtual y completar el formulario de solicitud.", "Académico"),
                ("¿Cómo reviso mis notas?", "Puedes revisar tus notas en el portal estudiantil con tu carné y contraseña.", "Académico"),
                ("¿Qué hago si repruebo un curso?", "Debes esperar al siguiente periodo de inscripción para repetir el curso.", "Académico"),
                ("¿Cómo solicito una revisión de examen?", "Debes presentar una solicitud formal al catedrático dentro de los 3 días hábiles.", "Académico"),
                ("¿Cuál es el mínimo de nota para aprobar?", "La nota mínima para aprobar un curso es 61 puntos sobre 100.", "Académico"),
                # Técnico
                ("¿Cómo recupero mi contraseña?", "Debes ir a la opción de recuperar contraseña en el portal e ingresar tu correo institucional.", "Técnico"),
                ("¿Qué navegadores son compatibles?", "El portal es compatible con Chrome, Firefox, Edge y Safari en sus versiones más recientes.", "Técnico"),
                ("¿Cómo accedo al correo institucional?", "Puedes acceder en mail.usac.edu.gt con tus credenciales de estudiante.", "Técnico"),
                ("¿Qué hago si el portal no carga?", "Verifica tu conexión a internet, limpia el caché del navegador e intenta nuevamente.", "Técnico"),
                ("¿Cómo instalo el software requerido?", "Los instaladores están disponibles en el portal estudiantil en la sección de descargas.", "Técnico"),
                ("¿Cómo reporto un problema técnico?", "Puedes reportar problemas al correo soporte.ti@usac.edu.gt o llamar al 2418-8000.", "Técnico"),
            ]
            for pregunta, respuesta, categoria in preguntas:
                q = Question(
                    question_text=pregunta,
                    answer_text=respuesta,
                    category_id=cat_ids.get(categoria)
                )
                db.add(q)
            db.commit()
            print("✅ 20 preguntas cargadas")

        # --- Config inicial ---
        if not db.query(BotConfig).first():
            db.add(BotConfig(chat_id=None))
            db.commit()
            print("✅ Config inicial creada")

    except Exception as e:
        print(f"❌ Error en seed: {e}")
        db.rollback()
    finally:
        db.close()