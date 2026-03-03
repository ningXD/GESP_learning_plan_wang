from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from extensions import db, jwt, cors

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(__file__), 'config', '.env'))

app = Flask(__name__, static_folder='../frontend', static_url_path='')

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

# JWT配置
@app.route('/api/test-token')
def test_token():
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=1)
    return jsonify({'token': token})

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
from routes.compile import bp as compile_bp
from routes.course import course_bp as course_bp
from routes.study_plan import study_plan_bp
app.register_blueprint(auth_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(users_bp)
app.register_blueprint(compile_bp)
app.register_blueprint(course_bp)
app.register_blueprint(study_plan_bp)

if __name__ == '__main__':
    try:
        # 创建数据库表
        with app.app_context():
            from models.models import User, Note, Student, ClassRecord, CourseRecord, StudyPlan, StudyPlanWeek
            
            # 检查是否已存在demo账号
            demo_user = User.query.filter_by(username='demo').first()
            if not demo_user:
                # 创建表
                db.create_all()
                # 初始化demo账号
                import bcrypt
                # 创建demo账号（管理员）
                hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                demo_user = User(
                    username='demo',
                    password=hashed_password,
                    role='admin',
                    admin=True
                )
                db.session.add(demo_user)
                
                # 创建教师测试账号
                teacher_hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                teacher_user = User(
                    username='teacher_test',
                    password=teacher_hashed_password,
                    nickname='测试教师',
                    role='teacher',
                    admin=False
                )
                db.session.add(teacher_user)
                
                # 初始化学生账号和学习计划
                from scripts.init_study_plan import init_study_plan_template
                init_study_plan_template()
                
                # 创建学生测试账号
                student_hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                student_user = User(
                    username='student_test',
                    password=student_hashed_password,
                    nickname='测试学生',
                    role='student',
                    admin=False,
                    age=16,
                    gender='男',
                    grade='高二',
                    subject='编程竞赛'
                )
                db.session.add(student_user)
                
                db.session.commit()
                print("Demo account created successfully")
                print("Teacher test account created successfully")
                print("Student test account created successfully")
            else:
                print("Database already initialized")
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()