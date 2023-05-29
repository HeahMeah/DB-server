import psycopg2

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = ''
db = SQLAlchemy(app)
CORS(app)


class Cases(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_summary = db.Column(db.Text)

    # Relationships
    patient_objects = db.relationship('Patient', secondary='cp_objects', backref='case')
    disease_objects = db.relationship('Disease', secondary='cd_objects', backref='case')
    question_objects = db.relationship('QuestionType', secondary='cq_objects', backref='case')
    treatment_objects = db.relationship('Treatment', secondary='ct_objects', backref='case')

    def serialize(self):
        return {
            'id': self.id,
            'patient_summary': self.patient_summary,
            'patient_objects': [obj.serialize() for obj in self.patient_objects],
            'disease_objects': [obj.serialize() for obj in self.disease_objects],
            'question_objects': [obj.serialize() for obj in self.question_objects],
            'treatment_objects': [obj.serialize() for obj in self.treatment_objects]
        }


class PatientQuestion(db.Model):
    __tablename__ = 'patient_question'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    question = db.Column(db.Text)

    #Realtionships
    patient_objects = db.relationship('Patient', secondary='cpq_patient_objects', backref='question')
    disease_objects = db.relationship('Disease', secondary='cpq_disease_objects', backref='question')
    question_objects = db.relationship('QuestionType', secondary='cpq_question_objects', backref='question')
    treatment_objects = db.relationship('Treatment', secondary='cpq_treatment_objects', backref='question')

    def serialize(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'question': self.question,
            'patient_objects': [obj.serialize() for obj in self.patient_objects],
            'disease_objects': [obj.serialize() for obj in self.disease_objects],
            'question_objects': [obj.serialize() for obj in self.question_objects],
            'treatment_objects': [obj.serialize() for obj in self.treatment_objects]
        }


class ProcessedQuestion(db.Model):
    __tablename__ = 'processed_question'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('patient_question.id'))
    question = db.Column(db.Text)
    question_note = db.Column(db.Text)

    # Relationships
    patient_objects = db.relationship('Patient', secondary='rq_patient_objects', backref='processed_question')
    disease_objects = db.relationship('Disease', secondary='rq_disease_objects', backref='processed_question')
    question_objects = db.relationship('QuestionType', secondary='rq_question_objects', backref='processed_question')
    treatment_objects = db.relationship('Treatment', secondary='rq_treatment_objects', backref='processed_question')


    def serialize(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'question_id': self.question_id,
            'question': self.question,
            'question_note': self.question_note,
            'patient_objects': [obj.serialize() for obj in self.patient_objects],
            'disease_objects': [obj.serialize() for obj in self.disease_objects],
            'question_objects': [obj.serialize() for obj in self.question_objects],
            'treatment_objects': [obj.serialize() for obj in self.treatment_objects],
        }


class Enhanced(db.Model):
    __tablename__ = 'enhanced'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    processed_question_id = db.Column(db.Integer, db.ForeignKey('processed_question.id'))


    #Relationships
    treatments = db.relationship('Treatment', secondary='enhanced_treatments', backref='enhanced')
    patients = db.relationship('Patient', secondary='enhanced_patients', backref='enhanced')
    diseases = db.relationship('Disease', secondary='enhanced_diseases', backref='enhanced')
    question_types = db.relationship('QuestionType', secondary='enhanced_question_types', backref='enhanced')

    def serialize(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'processed_question_id': self.processed_question_id,
            'treatments': [obj.serialize() for obj in self.treatments],
            'patients': [obj.serialize() for obj in self.patients],
            'diseases': [obj.serialize() for obj in self.diseases],
            'question_types': [obj.serialize() for obj in self.question_types],
        }


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    processed_question_id = db.Column(db.Integer, db.ForeignKey('processed_question.id'))
    reference = db.Column(db.Text)
    highlighted_text = db.Column(db.Text)
    alternative_pubmed_link = db.Column(db.Text)

    # Relationships
    patients_objects = db.relationship('Patient', secondary='articles_patient_objects', backref='article')
    diseases_objects = db.relationship('Disease', secondary='articles_disease_objects', backref='article')
    question_objects = db.relationship('QuestionType', secondary='articles_question_objects', backref='article')
    treatment_objects = db.relationship('Treatment', secondary='articles_treatment_objects', backref='article')

    def serialize(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'processed_question_id': self.processed_question_id,
            'reference': self.reference,
            'highlighted_text': self.highlighted_text,
            'alternative_pubmed_link': self.alternative_pubmed_link,
            'patients_objects': [obj.serialize() for obj in self.patients_objects],
            'diseases_objects': [obj.serialize() for obj in self.diseases_objects],
            'question_objects': [obj.serialize() for obj in self.question_objects],
            'treatment_objects': [obj.serialize() for obj in self.treatment_objects],
        }

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer)
    age_range = db.Column(db.Enum('less_18', 'from_18_to_29', 'from_30_to_39',
                                  'from_40_to_49', 'from_50_to_59', 'from_60_to_69', 'over_70', name='p_age'))
    gender = db.Column(db.Enum('male', 'female', name='p_gender'))

    # Relationships
    rq_patient_objects = db.relationship('RQPatientObj', backref='patient')
    cp_objects = db.relationship('CPObj', backref='patient')
    article_patient_objects = db.relationship('ArticlePatientObj', backref='patient')
    cpq_patient_objects = db.relationship('CPQPatientObj', backref='patient')
    enhanced_patients = db.relationship('EnhancedPatients', backref='patient')
    patient_symptoms = db.relationship('PatientSymptoms', backref='patient')
    patient_background_diseases = db.relationship('PatientBackgroundDiseases', backref='patient')
    patient_side_effects = db.relationship('PatientSideEffects', backref='patient')

    def serialize(self):
        return {
            'id': self.id,
            'age': self.age,
            'age_range': self.age_range,
            'gender': self.gender,
            'rq_patient_objects': [obj.serialize() for obj in self.rq_patient_objects],
            'cp_objects': [obj.serialize() for obj in self.cp_objects],
            'article_patient_objects': [obj.serialize() for obj in self.article_patient_objects],
            'cpq_patient_objects': [obj.serialize() for obj in self.cpq_patient_objects],
            'enhanced_patients': [obj.serialize() for obj in self.enhanced_patients],
            'patient_symptoms': [obj.serialize() for obj in self.patient_symptoms],
            'patient_background_diseases': [obj.serialize() for obj in self.patient_background_diseases],
            'patient_side_effects': [obj.serialize() for obj in self.patient_side_effects],
        }


class Symptom(db.Model):
    __tablename__ = 'symptom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    location = db.Column(db.Text)
    severity = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'severity': self.severity
        }


class PatientSymptoms(db.Model):
    __tablename__ = 'patient_symptoms'
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)

    def serialize(self):
        return {
            'symptom_id': self.symptom_id,
            'patient_id': self.patient_id
        }


class BackgroundDisease(db.Model):
    __tablename__ = 'background_disease'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class PatientBackgroundDiseases(db.Model):
    __tablename__ = 'patient_background_diseases'
    back_g_disease_id = db.Column(db.Integer, db.ForeignKey('background_disease.id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)

    def serialize(self):
        return {
            'back_g_disease_id': self.back_g_disease_id,
            'patient_id': self.patient_id
        }


class SideEffect(db.Model):
    __tablename__ = 'side_effect'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class PatientSideEffects(db.Model):
    __tablename__ = 'patient_side_effects'
    side_effect_id = db.Column(db.Integer, db.ForeignKey('side_effect.id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)

    def serialize(self):
        return {
            'side_effect_id': self.side_effect_id,
            'patient_id': self.patient_id
        }

class Disease(db.Model):
    __tablename__ = 'disease'
    id = db.Column(db.Text, primary_key=True)
    full_name = db.Column(db.Text)
    shortcut = db.Column(db.Text)

    # Relationships
    cd_objects = db.relationship('CDObj', backref='disease')
    rq_disease_objects = db.relationship('RQDiseaseObj', backref='disease')
    article_disease_objects = db.relationship('ArticleDiseaseObj', backref='disease')
    cpq_disease_objects = db.relationship('CPQDiseaseObj', backref='disease')
    enhanced_diseases = db.relationship('EnhancedDiseases', backref='disease')
    disease_m = db.relationship('DiseaseM', backref='disease')
    disease_l = db.relationship('DiseaseL', backref='disease')
    disease_p = db.relationship('DiseaseP', backref='disease')

    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'shortcut': self.shortcut
        }


class DiseaseProtein(db.Model):
    __tablename__ = 'disease_protein'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class DiseaseP(db.Model):
    __tablename__ = 'disease_p'
    disease_id = db.Column(db.Text, db.ForeignKey('disease.id'), primary_key=True)
    protein_id = db.Column(db.Integer, db.ForeignKey('disease_protein.id'), primary_key=True)

    def serialize(self):
        return {
            'disease_id': self.disease_id,
            'protein_id': self.protein_id
        }


class DiseaseLocation(db.Model):
    __tablename__ = 'disease_location'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'location': self.location
        }


class DiseaseL(db.Model):
    __tablename__ = 'disease_l'
    location_id = db.Column(db.Integer, db.ForeignKey('disease_location.id'), primary_key=True)
    disease_id = db.Column(db.Text, db.ForeignKey('disease.id'), primary_key=True)

    def serialize(self):
        return {
            'location_id': self.location_id,
            'disease_id': self.disease_id
        }


class DiseaseMutation(db.Model):
    __tablename__ = 'disease_mutation'
    id = db.Column(db.Integer, primary_key=True)
    mutation = db.Column(db.Text)
    mutation_status = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'mutation': self.mutation,
            'mutation_status': self.mutation_status
        }


class DiseaseM(db.Model):
    __tablename__ = 'disease_m'
    mutation_id = db.Column(db.Integer, db.ForeignKey('disease_mutation.id'), primary_key=True)
    disease_id = db.Column(db.Text, db.ForeignKey('disease.id'), primary_key=True)


    def serialize(self):
        return {
            'mutation_id': self.mutation_id,
            'disease_id': self.disease_id
        }


class QuestionType(db.Model):
    __tablename__ = 'question_type'
    id = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text)
    classification = db.Column(db.Text)

    # Relationships
    cq_objects = db.relationship('CQObj', backref='question_type')
    rq_question_objects = db.relationship('RQQuestionObj', backref='question_type')
    article_question_objects = db.relationship('ArticleQuestionObj', backref='question_type')
    cpq_question_objects = db.relationship('CPQQuestionObj', backref='question_type')
    enhanced_question_types = db.relationship('EnhancedQuestionTypes', backref='question_type')


    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'classification': self.classification
        }


class Treatment(db.Model):
    __tablename__ = 'treatment'
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    treatment_type = db.Column(db.Text)
    sub_classification = db.Column(db.Text)

    # Relationships
    enhanced_treatments = db.relationship('EnhancedTreatments', backref='treatment')
    cpq_treatment_objects = db.relationship('CPQTreatmentObj', backref='treatment')
    article_treatment_objects = db.relationship('ArticleTreatmentObj', backref='treatment')
    rq_treatment_objects = db.relationship('RQTreatmentObj', backref='treatment')
    ct_objects = db.relationship('CTObj', backref='treatment')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'treatment_type': self.treatment_type,
            'sub_classification': self.sub_classification
        }


# Associated Tables for Cases

class CPObj(db.Model):
    __tablename__ = 'cp_objects'
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key=True)
    p_object_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)


class CDObj(db.Model):
    __tablename__ = 'cd_objects'
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key=True)
    disease_object_id = db.Column(db.Text, db.ForeignKey('disease.id'), primary_key=True)


class CQObj(db.Model):
    __tablename__ = 'cq_objects'
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key=True)
    question_object_id = db.Column(db.Text, db.ForeignKey('question_type.id'), primary_key=True)


class CTObj(db.Model):
    __tablename__ = 'ct_objects'
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), primary_key=True)
    treatment_object_id = db.Column(db.Text, db.ForeignKey('treatment.id'), primary_key=True)


# Associated Tables for Processed Question

class RQPatientObj(db.Model):
    __tablename__ = 'rq_patient_objects'
    research_question_id = db.Column(db.Integer, db.ForeignKey('processed_question.id'), primary_key=True)
    patient_object_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)

class RQDiseaseObj(db.Model):
    __tablename__ = 'rq_disease_objects'
    research_question_id = db.Column(db.Integer, db.ForeignKey('processed_question.id'), primary_key=True)
    disease_object_id = db.Column(db.Text, db.ForeignKey('disease.id'), primary_key=True)


class RQQuestionObj(db.Model):
    __tablename__ = 'rq_question_objects'
    research_question_id = db.Column(db.Integer, db.ForeignKey('processed_question.id'), primary_key=True)
    question_object_id = db.Column(db.Text, db.ForeignKey('question_type.id'), primary_key=True)


class RQTreatmentObj(db.Model):
    __tablename__ = 'rq_treatment_objects'
    research_question_id = db.Column(db.Integer, db.ForeignKey('processed_question.id'), primary_key=True)
    treatment_object_id = db.Column(db.Text, db.ForeignKey('treatment.id'), primary_key=True)


# Associated Tables for Articles

class ArticlePatientObj(db.Model):
    __tablename__ = 'articles_patient_objects'
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
    patient_object_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)


class ArticleDiseaseObj(db.Model):
    __tablename__ = 'articles_disease_objects'
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
    disease_object_id = db.Column(db.Text, db.ForeignKey('disease.id'), primary_key=True)


class ArticleQuestionObj(db.Model):
    __tablename__ = 'articles_question_objects'
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
    question_object_id = db.Column(db.Text, db.ForeignKey('question_type.id'), primary_key=True)


class ArticleTreatmentObj(db.Model):
    __tablename__ = 'articles_treatment_objects'
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
    treatment_object_id = db.Column(db.Text, db.ForeignKey('treatment.id'), primary_key=True)


# Associated Tables for Patient Question

class CPQPatientObj(db.Model):
    __tablename__ = 'cpq_patient_objects'
    question_id = db.Column(db.Integer, db.ForeignKey('patient_question.id'), primary_key=True)
    patient_object_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)


class CPQDiseaseObj(db.Model):
    __tablename__ = 'cpq_disease_objects'
    question_id = db.Column(db.Integer, db.ForeignKey('patient_question.id'), primary_key=True)
    disease_object_id = db.Column(db.Text, db.ForeignKey('disease.id'), primary_key=True)


class CPQQuestionObj(db.Model):
    __tablename__ = 'cpq_question_objects'
    question_id = db.Column(db.Integer, db.ForeignKey('patient_question.id'), primary_key=True)
    question_object_id = db.Column(db.Text, db.ForeignKey('question_type.id'), primary_key=True)


class CPQTreatmentObj(db.Model):
    __tablename__ = 'cpq_treatment_objects'
    question_id = db.Column(db.Integer, db.ForeignKey('patient_question.id'), primary_key=True)
    treatment_object_id = db.Column(db.Text, db.ForeignKey('treatment.id'), primary_key=True)


# Associated Tables for Enhanced

class EnhancedTreatments(db.Model):
    __tablename__ = 'enhanced_treatments'
    enhanced_id = db.Column(db.Integer, db.ForeignKey('enhanced.id'), primary_key=True)
    treatment_id = db.Column(db.Text, db.ForeignKey('treatment.id'), primary_key=True)


class EnhancedPatients(db.Model):
    __tablename__ = 'enhanced_patients'
    enhanced_id = db.Column(db.Integer, db.ForeignKey('enhanced.id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)


class EnhancedDiseases(db.Model):
    __tablename__ = 'enhanced_diseases'
    enhanced_id = db.Column(db.Integer, db.ForeignKey('enhanced.id'), primary_key=True)
    disease_id = db.Column(db.Text, db.ForeignKey('disease.id'), primary_key=True)


class EnhancedQuestionTypes(db.Model):
    __tablename__ = 'enhanced_question_types'
    enhanced_id = db.Column(db.Integer, db.ForeignKey('enhanced.id'), primary_key=True)
    question_type_id = db.Column(db.Text, db.ForeignKey('question_type.id'), primary_key=True)


#routes

@app.route('/api/patient_question', methods=['GET'])
def get_patient_question():
    patient_questions = PatientQuestion.query.all()
    return jsonify([question.serialize() for question in patient_questions])

@app.route('/api/processed_question', methods=['GET'])
def get_processed_question():
    processed_questions = ProcessedQuestion.query.all()
    return jsonify([question.serialize() for question in processed_questions])

@app.route('/api/enhanced', methods=['GET'])
def get_enhanced():
    enhanced_data = Enhanced.query.all()
    return jsonify([enhanced.serialize() for enhanced in enhanced_data])

@app.route('/api/articles', methods=['GET'])
def get_articles():
    articles = Articles.query.all()
    return jsonify([article.serialize() for article in articles])

@app.route('/api/patient', methods=['GET'])
def get_patient():
    patients = Patient.query.all()
    return jsonify([patient.serialize() for patient in patients])

@app.route('/api/question_type', methods=['GET'])
def get_question_type():
    question_types = QuestionType.query.all()
    return jsonify([question_type.serialize() for question_type in question_types])

@app.route('/api/treatment', methods=['GET'])
def get_treatment():
    treatments = Treatment.query.all()
    return jsonify([treatment.serialize() for treatment in treatments])

@app.route('/api/disease', methods=['GET'])
def get_disease():
    diseases = Disease.query.all()
    return jsonify([disease.serialize() for disease in diseases])


#Trying display all items related to same case id
@app.route('/api/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    # Fetch the case by id
    case = Cases.query.get(case_id)

    if not case:
        return jsonify({'message': 'Case not found'}), 404

    # Fetch related entities for Cases
    patients = [p.serialize() for p in case.patient_objects]
    diseases = [d.serialize() for d in case.disease_objects]
    questions = [q.serialize() for q in case.question_objects]
    treatments = [t.serialize() for t in case.treatment_objects]

    # Fetch related entities for each PatientQuestion related to the case
    patient_questions_data = []
    patient_questions = PatientQuestion.query.filter_by(case_id=case.id).all()
    for pq in patient_questions:
        patient_questions_data.append({
            'patient_question': pq.serialize(),
            'patient_objects': [po.serialize() for po in pq.patient_objects],
            'disease_objects': [do.serialize() for do in pq.disease_objects],
            'question_objects': [qo.serialize() for qo in pq.question_objects],
            'treatment_objects': [to.serialize() for to in pq.treatment_objects],
        })

    # Fetch related entities for each ProcessedQuestion related to the case
    processed_questions_data = []
    processed_questions = ProcessedQuestion.query.filter_by(case_id=case.id).all()
    for pq in processed_questions:
        processed_questions_data.append({
            'processed_question': pq.serialize(),
            'patient_objects': [po.serialize() for po in pq.patient_objects],
            'disease_objects': [do.serialize() for do in pq.disease_objects],
            'question_objects': [qo.serialize() for qo in pq.question_objects],
            'treatment_objects': [to.serialize() for to in pq.treatment_objects],
        })

    # Fetch related entities for each Enhanced related to the case
    enhanced_data = []
    enhanced_objects = Enhanced.query.filter_by(case_id=case.id).all()
    for e in enhanced_objects:
        enhanced_data.append({
            'enhanced': e.serialize(),
            'treatments': [t.serialize() for t in e.treatments],
            'patients': [p.serialize() for p in e.patients],
            'diseases': [d.serialize() for d in e.diseases],
            'question_types': [qt.serialize() for qt in e.question_types],
        })

    # Fetch related entities for each Article related to the case
    articles_data = []
    articles = Articles.query.filter_by(case_id=case.id).all()
    for a in articles:
        articles_data.append({
            'article': a.serialize(),
            'patients_objects': [po.serialize() for po in a.patients_objects],
            'diseases_objects': [do.serialize() for do in a.diseases_objects],
            'question_objects': [qo.serialize() for qo in a.question_objects],
            'treatment_objects': [to.serialize() for to in a.treatment_objects],
        })

    # Return the result as JSON
    return jsonify({
        'case': case.serialize(),
        'patients': patients,
        'diseases': diseases,
        'questions': questions,
        'treatments': treatments,
        'patient_questions': patient_questions_data,
        'processed_questions': processed_questions_data,
        'enhanced_objects': enhanced_data,
        'articles': articles_data,
    })