import bcrypt

def hash_password(password):
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed  # Keep it in byte format for secure storage

def verify_password(password, hashed):
    """Verifies a password against a stored hash."""
    return bcrypt.checkpw(password.encode(), hashed)
