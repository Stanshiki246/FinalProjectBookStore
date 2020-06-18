from app import app,db
from app.models.Users import Users
from app.models.Products import Products

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Products': Products}
