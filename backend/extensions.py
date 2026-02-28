from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()