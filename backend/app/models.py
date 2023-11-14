from datetime import datetime, timezone

from app import db

# utility
nowf = lambda: datetime.now(timezone.utc)


class Student(db.Model):
    reg_no = db.Column(
        db.String(9), 
        primary_key=True)
    photo = db.Column(db.LargeBinary)

    def __repr__(self) -> str:
        return f'Student regno: {self.reg_no}'
        

class Course(db.Model):
    cid = db.Column(
        db.String(15), 
        primary_key=True)
    code = db.Column(db.String(10))
    room = db.Column(db.Integer)
    block = db.Column(db.String(5))
    faculty_id = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f'Course {self.cid} - {self.code}, {self.block}: {self.room}'
    

class Attendence(db.Model):
    id = db.Column(
        db.BigInteger().with_variant(db.Integer, "sqlite"), 
        primary_key=True)
    date = db.Column(
        db.DateTime, 
        default=nowf,
        onupdate=nowf)
    present = db.Column(
        db.Boolean,
        default=False)
    
    # foreign keys
    course_cid = db.Column(
        db.String(15),
        db.ForeignKey('course.cid'))
    student_reg_no = db.Column(
        db.String(9),
        db.ForeignKey('student.reg_no'))
    
    def __repr__(self) -> str:
        return f'Attendence {self.student_reg_no} - {self.course_cid} {self.date}: {self.present}'
    

    
    

