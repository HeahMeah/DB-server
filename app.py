import psycopg2

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:Rokandroolfaq1!@localhost/LocalDB'
db = SQLAlchemy(app)
CORS(app)


class Cases(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_summary = db.Column(db.String(2550))
    def Cases_dict(self):
        return {
            'id': self.id,
            'P_Sum': self.patient_summary,
        }

class CasePatientQuestions(db.Model):
    __tablename__ = 'case_patient_questions'
    question_id  = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    question = db.Column(db.String(2550))

    def to_dict(self):
        return {
            'ID': self.question_id,
            'Case_ID': self.case_id,
            'Question': self.question
        }


class ResearchQuestionProcessed(db.Model):
    __tablename__ = 'research_question_processed'
    research_question_id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('case_patient_questions.question_id'))
    question = db.Column(db.String(2550))
    question_note = db.Column(db.String(2550))

    def to_dict(self):
        return{
            'Case ID': self.case_id,
            'ID': self.research_question_id,
            'Question': self.question,
            'Note': self.question_note
        }


class Enchanced(db.Model):
    __tablename__ = 'enchanced'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    research_question_id = db.Column(db.Integer, db.ForeignKey('research_question_processed.research_question_id'))
    patient = db.Column(db.String(2550))
    disease = db.Column(db.Text, db.ForeignKey('disease_table.object_id'))
    treatment = db.Column(db.Text, db.ForeignKey('treatment_table.object_id'))
    question_type = db.Column(db.Text,db.ForeignKey('question_types.object_id'))

    def to_dict(self):
        return {
            'ID': self.id,
            'Case ID' : self.case_id,
            'Research question ID': self.research_question_id,
            'Patient' : self.patient,
            'Disease' : self.disease,
            'Treatment' : self.treatment,
            'Question Type' : self.question_type

        }


class Articles(db.Model):
    __tablename__ = 'articles'
    article_id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    research_question_id = db.Column(db.Integer, db.ForeignKey('research_question_processed.research_question_id'))
    reference = db.Column(db.String(2550))
    highlighted_text = db.Column(db.String(2550))
    alternative_pubmed_link = db.Column(db.String(2550))

    def to_dict(self):
        return {
            'Articles ID' : self.article_id,
            'Case ID' : self.case_id,
            'Research question ID': self.research_question_id,
            'Reference' : self.reference,
            'Highlighted text' : self.highlighted_text,
            'Alternative Link' : self.alternative_pubmed_link

        }


class PatientTable(db.Model):
    __tablename__ = 'patient_table'
    object_id = db.Column(db.Text, primary_key=True)
    object_name = db.Column(db.String(2550))
    object_classification = db.Column(db.String(2550))
    object_sub_classification = db.Column(db.String(2550))

    def to_dict(self):
        return {
            'Object ID' : self.object_classification,
            'Object name' : self.object_name,
            'Object classification' : self.object_classification,
            'Object subclassification' : self.object_sub_classification
        }


class DiseaseTable(db.Model):
    __tablename__ = 'disease_table'
    object_id = db.Column(db.Text, primary_key=True)
    object_name = db.Column(db.String(2550))
    object_classification = db.Column(db.String(2550))
    object_sub_classification = db.Column(db.String(2550))

    def to_dict(self):
        return {
            'Object ID': self.object_classification,
            'Object name': self.object_name,
            'Object classification': self.object_classification,
            'Object subclassification': self.object_sub_classification
        }


class QuestionTypes(db.Model):
    __tablename__ = 'question_types'
    object_id = db.Column(db.Text, primary_key=True)
    object_name = db.Column(db.String(2550))
    object_classification = db.Column(db.String(2550))
    object_sub_classification = db.Column(db.String(2550))

    def to_dict(self):
        return {
            'Object ID': self.object_classification,
            'Object name': self.object_name,
            'Object classification': self.object_classification,
            'Object subclassification': self.object_sub_classification
        }


class Treatments(db.Model):
    __tablename__ = 'treatments'
    object_id = db.Column(db.Text, primary_key=True)
    object_name = db.Column(db.String(2550))
    object_classification = db.Column(db.String(2550))
    object_sub_classification = db.Column(db.String(2550))
    object_sub_classification_2 = db.Column(db.String(2550))

    def to_dict(self):
        return {
            'Object ID': self.object_id,
            'Object name': self.object_name,
            'Object classification': self.object_classification,
            'Object subclassification': self.object_sub_classification,
            'Object subclassification2' : self.object_sub_classification_2
        }


class CaseDisease(db.Model):
   __tablename__ = 'case_disease'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
   disease_id = db.Column(db.Text, db.ForeignKey('disease_table.object_id'))


class CaseTreatment(db.Model):
    __tablename__ = 'case_treatment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    treatment_id = db.Column(db.Text, db.ForeignKey('treatments.object_id'))


class CaseQuestionType(db.Model):
    __tablename__ = 'case_question_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    question_type_id = db.Column(db.Integer, db.ForeignKey('question_types.object_id'))


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255),  nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime)

    actions = db.relationship("UserActions", back_populates="user")


class UserActions(db.Model):
    __tablename__ = 'user_actions'
    action_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'))
    action_type = db.Column(db.String(2550))
    action_description = db.Column(db.String(2550))
    action_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship("Users", back_populates="actions")

# Associations tables for Cases
class CPObjects(db.Model):
    __tablename__ = 'cp_objects'
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key=True)
    patient_object_id = db.Column(db.Text, db.ForeignKey('patient_table.object_id'), primary_key=True)

    case = db.relationship('cases', backref='cp_objects')
    patient = db.relationship('patient_table', backref='cp_objects')

class CDObjects(db.model):
    __tablename__ = 'cd_objects'
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key=True)
    disease_object_id = db.Column(db.Text, db.ForeignKey('disease_table.object_id'), primary_key=True)

    case = db.relationship('cases', backref='cd_objects')
    disease = db.relationship('disease_table', backref='cd_objects')

class CQObjects(db.model):
    __tablename__ = 'cq_objects'
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key=True)
    question_object_id = db.Column(db.Text, db.ForeignKey('question_types.object_id'), primary_key=True)

    case = db.relationship('cases', backref='cq_objects')
    question = db.relationship()

class CTObjects(db.Model):
    __tablename__ = 'ct_objects'
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key=True)
    treatment_object_id = db.Column(db.Text, db.ForeignKey('treatments.object_id'), primary_key=True)

    case = db.relationship('cases', backref='cd_disease')
    treatments = db.relationship()




#routes

@app.route('/api/Case_patient_questions', methods=['GET'])
def get_CPQ():
    P_questions = CasePatientQuestions.query.all()
    return jsonify([question.to_dict() for question in P_questions])

@app.route('/api/Research_Question_Processed', methods=['GET'])
def get_RQP():
    R_questions = ResearchQuestionProcessed.query.all()
    return jsonify([question.to_dict() for question in R_questions])

@app.route('/api/Treatments', methods=['GET'])
def get_treatments():
    treatments = Treatments.query.all()
    return jsonify([treatment.to_dict() for treatment in treatments])

@app.route('/api/enchanced', methods=['GET'])
def get_enchanced():
    ench = Enchanced.query.all()
    return jsonify([e.to_dict() for e in ench])

@app.route('/api/articles', methods=['GET'])
def get_articles():
    article = Articles.query.all()
    return jsonify([art.to_dict() for art in article])

@app.route('/api/patients', methods=['GET'])
def get_patients():
    patient = Patients.query.all()
    return jsonify([pat.to_dict() for pat in patient])

@app.route('/api/disease', methods=['GET'])
def get_disease():
    dis = Disease.query.all()
    return jsonify([d.to_dict() for d in dis])

@app.route('/api/questions', methods=['GET'])
def get_questuions():
    question = Questions.query.all()
    return jsonify([quest.to_dict() for quest in question])
