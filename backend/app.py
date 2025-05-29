from flask import Flask
from flask_cors import CORS
from db import db
from routes.group_routes import group_bp
from routes.user_routes import user_bp
from routes.expense_routes import expense_bp

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://splitcloneuser:your-secure-password@splitclone-db.c8zcg6iy0xhq.us-east-1.rds.amazonaws.com:5432/splitclone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(group_bp)
app.register_blueprint(user_bp)
app.register_blueprint(expense_bp)

@app.route("/")
def health_check():
    return "OK", 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)

