from app import app,db

@app.errorhandler(404)
def not_found_404(error):
    return "Error 404",404

@app.errorhandler(500)
def internal_500(error):
    db.session.rollback()
    return "Internal Error 500",500

