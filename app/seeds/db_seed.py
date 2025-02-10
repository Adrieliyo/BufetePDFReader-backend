from app.config.database import SessionLocal
from app.models.roles import Role
from app.models.user_status import UserStatus

def seed_initial_data():
    db = SessionLocal()
    try:
        # Insertar roles si no existen
        roles = [
            {"role": "Administrator"},
            {"role": "Client"}
        ]
        
        for role_data in roles:
            role = db.query(Role).filter_by(role=role_data["role"]).first()
            if not role:
                role = Role(**role_data)
                db.add(role)
        
        # Insertar estados de usuario si no existen
        statuses = [
            {"status": "Active"},
            {"status": "Inactive"}
        ]
        
        for status_data in statuses:
            status = db.query(UserStatus).filter_by(status=status_data["status"]).first()
            if not status:
                status = UserStatus(**status_data)
                db.add(status)
        
        db.commit()
        print("Datos base insertados correctamente")
        
    except Exception as e:
        print(f"Error insertando datos base: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_initial_data()