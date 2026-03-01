try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_jwt_extended import JWTManager
    from flask_cors import CORS
    import pymysql
    from dotenv import load_dotenv
    print("所有依赖包导入成功！")
    
    # 测试Flask应用创建
    app = Flask(__name__)
    print("Flask应用创建成功！")
    
    # 测试配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/gesp_study_plan'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    print("应用配置成功！")
    
    # 测试扩展初始化
    db = SQLAlchemy(app)
    jwt = JWTManager(app)
    CORS(app, origins=['*'])
    print("扩展初始化成功！")
    
    print("所有测试通过！Flask环境配置正确。")
    
except ImportError as e:
    print(f"导入错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
    import traceback
    traceback.print_exc()
