from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # 用户账号，用于登录，唯一
    password = db.Column(db.String(255), nullable=False)  # 密码，加密存储
    email = db.Column(db.String(100), unique=True, nullable=True)  # 邮箱，唯一
    phone = db.Column(db.String(20), unique=True, nullable=True)  # 手机号，唯一，可用于登录
    nickname = db.Column(db.String(50), nullable=True, index=True)  # 用户姓名，用于显示，添加索引提高搜索性能
    role = db.Column(db.String(20), nullable=False, default='student')  # student, teacher, admin
    admin = db.Column(db.Boolean, nullable=False, default=False)  # 是否为管理员
    age = db.Column(db.Integer, nullable=True)  # 年龄
    gender = db.Column(db.String(10), nullable=True)  # 性别
    grade = db.Column(db.String(20), nullable=True)  # 年级
    subject = db.Column(db.String(50), nullable=True)  # 学科/学习项目
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    # 关系
    notes = db.relationship('Note', backref='user', lazy=True)
    students = db.relationship('Student', backref='teacher', lazy=True)
    class_records = db.relationship('ClassRecord', backref='teacher', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone or '',
            'nickname': self.nickname or '',
            'role': self.role,
            'admin': self.admin,
            'age': self.age or 0,
            'gender': self.gender or '',
            'grade': self.grade or '',
            'subject': self.subject or '',
            'created_at': self.created_at.isoformat()
        }

class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(20), nullable=False)  # text, image, mindmap
    images = db.Column(db.JSON, nullable=True)  # 存储图片路径数组
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'images': self.images,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(20), nullable=True)
    project = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    remaining_classes = db.Column(db.Integer, default=0)  # 剩余课时数
    remaining_fee = db.Column(db.Float, default=0.0)  # 剩余学费
    enrollment_date = db.Column(db.Date, nullable=True)  # 入学时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 信息录入时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    class_records = db.relationship('ClassRecord', backref='student', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'grade': self.grade,
            'project': self.project,
            'phone': self.phone,
            'remaining_classes': self.remaining_classes,
            'remaining_fee': self.remaining_fee,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=True)  # 教师名称
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    teaching_subject = db.Column(db.String(50), nullable=True)  # 教学项目
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='teacher_profile', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'phone': self.phone,
            'teaching_subject': self.teaching_subject,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ClassRecord(db.Model):
    __tablename__ = 'class_records'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id,
            'date': self.date.isoformat() if self.date else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'topic': self.topic,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CourseRecord(db.Model):
    __tablename__ = 'course_records'
    
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_records.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='completed')  # completed, cancelled, missed
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'class_id': self.class_id,
            'student_id': self.student_id,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudyPlan(db.Model):
    __tablename__ = 'study_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    plan_weeks = db.relationship('StudyPlanWeek', backref='study_plan', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'plan_weeks': [week.to_dict() for week in self.plan_weeks]
        }

class StudyPlanWeek(db.Model):
    __tablename__ = 'study_plan_weeks'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('study_plans.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    core_knowledge = db.Column(db.Text, nullable=True)
    practice = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'plan_id': self.plan_id,
            'week_number': self.week_number,
            'date': self.date.isoformat() if self.date else None,
            'topic': self.topic,
            'core_knowledge': self.core_knowledge,
            'practice': self.practice,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }