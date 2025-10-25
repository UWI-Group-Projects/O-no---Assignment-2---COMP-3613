from flask_login import current_user

def add_auth_context(app):
    @app.context_processor
    def inject_auth_context():
        # This lets templates use {{ current_user }} or similar
        from flask_login import current_user
        return dict(current_user=current_user)
