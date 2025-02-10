from sqlalchemy.types import TypeDecorator, DateTime
from datetime import datetime
import pytz

# Definir la zona horaria predeterminada
TIMEZONE = pytz.timezone("America/Mazatlan")

class TimezoneAware(TypeDecorator):
    """Tipo de dato personalizado para manejar timestamps con zona horaria."""
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Convierte los valores a UTC antes de almacenarlos en la base de datos."""
        if value is not None:
            if not value.tzinfo:
                value = TIMEZONE.localize(value)  # Asigna la zona horaria si no la tiene
            return value.astimezone(pytz.UTC)  # Guarda en UTC
        return value

    def process_result_value(self, value, dialect):
        """Convierte los valores de UTC a la zona horaria local al recuperar datos."""
        if value is not None:
            return value.replace(tzinfo=pytz.UTC).astimezone(TIMEZONE)  # Convierte de UTC a la zona horaria local
        return value