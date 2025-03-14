from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum("agent", "central_reader", "super_admin"), nullable=False)
    center_code = Column(String, ForeignKey("centers.center_code"), nullable=False)

class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, index=True)
    patient_mask_id = Column(String, unique=True, nullable=False)
    gender = Column(Enum("Male", "Female", "Other"), nullable=False)
    trial_id = Column(Enum("ALTER_UC", "ALTER_CD", "BOOST_UC", "BOOST_CD"), nullable=False)
    center_code = Column(String, ForeignKey("centers.center_code"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submission_time = Column(TIMESTAMP)
    test_id = Column(String, unique=True, nullable=False)
    agent_score = Column(Float, nullable=False)
    final_score = Column(Float, nullable=True)
    status = Column(Enum("pending", "finalized"), default="pending")
    agent_review = Column(Text, nullable=True)

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=False)
    reader_review = Column(Text, nullable=True)
    status = Column(Enum("pending", "confirmed"), default="pending")

class ScoreValidation(Base):
    __tablename__ = "score_validation"
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    agent_score = Column(Float, nullable=False)
    reader1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reader1_score = Column(Float, nullable=False)
    reader2_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reader2_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=False)
    status = Column(Enum("pending", "finalized"), default="pending")
