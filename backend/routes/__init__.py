from .auth import bp as auth_bp
from .notes import bp as notes_bp
from .users import bp as users_bp

__all__ = ['auth_bp', 'notes_bp', 'users_bp']