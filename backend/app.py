from flask import Flask
import os
from dotenv import load_dotenv
from extensions import db, jwt, cors

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 配置应用
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))

# 创建上传目录
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 初始化扩展
db.init_app(app)
jwt.init_app(app)
cors.init_app(app, origins=['*'])

# 错误处理
@app.errorhandler(404)
def not_found_error(error):
    return {'error': 'Resource not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return {'error': 'Internal server error'}, 500

# 导入并注册蓝图
from routes.auth import bp as auth_bp
from routes.notes import bp as notes_bp
from routes.users import bp as users_bp
app.register_blueprint(auth_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(users_bp)

if __name__ == '__main__':
    try:
        # 创建数据库表
        with app.app_context():
            db.create_all()
            # 初始化demo账号
            from models import User
            import bcrypt
            # 检查demo账号是否存在
            demo_user = User.query.filter_by(username='demo').first()
            if not demo_user:
                # 创建demo账号
                hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                demo_user = User(
                    username='demo',
                    password=hashed_password,
                    role='teacher',
                    admin=True
                )
                db.session.add(demo_user)
                db.session.commit()
                print("Demo account created successfully")
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()