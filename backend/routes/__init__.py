def register_blueprints(app):
    from routes.auth import auth_bp
    from routes.projects import projects_bp
    from routes.comments import comments_bp
    from routes.upload import upload_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(comments_bp, url_prefix="/api")
    app.register_blueprint(upload_bp, url_prefix="/api")
