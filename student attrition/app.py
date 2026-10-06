from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pandas as pd
import numpy as np
import google.generativeai as genai
from auth import login_user, register_user, log_assessment
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-in-production'

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✓ Gemini API configured")
else:
    print("⚠ Warning: GEMINI_API_KEY not found")

# Load student data
try:
    df_students = pd.read_csv('student_attrition_data.csv')
    print(f"✓ Loaded {len(df_students)} student records")
except:
    print("⚠ student_attrition_data.csv not found. Run generate_data.py first!")
    df_students = None

def analyze_attrition_risk_with_ai(student_data):
    """Use Gemini AI to analyze student attrition risk"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""You are an expert educational analyst specializing in student attrition risk assessment and retention strategies.

**Student Profile:**
- ID: {student_data.get('student_id', 'N/A')}
- Name: {student_data.get('name', 'N/A')}
- Program: {student_data.get('program', 'N/A')}
- Semester: {student_data.get('semester', 'N/A')}
- Department: {student_data.get('department', 'N/A')}

**Academic Performance:**
- Attendance: {student_data.get('attendance_percentage', 0):.1f}%
- Internal Assessment 1: {student_data.get('internal_marks_1', 0):.1f}/100
- Internal Assessment 2: {student_data.get('internal_marks_2', 0):.1f}/100
- Internal Assessment 3: {student_data.get('internal_marks_3', 0):.1f}/100
- Assignment Score: {student_data.get('assignment_score', 0):.1f}/100
- Project Score: {student_data.get('project_score', 0):.1f}/100
- Previous Semester CGPA: {student_data.get('previous_semester_cgpa', 0):.2f}/10
- Previous Year %: {student_data.get('previous_year_percentage', 0):.1f}%
- Backlogs: {student_data.get('backlogs', 0)}

**Financial Status:**
- Fee Payment: {student_data.get('fee_payment_status', 'N/A')}
- Scholarship: {student_data.get('scholarship', 'N/A')}
- Financial Difficulty: {student_data.get('financial_difficulty', 'N/A')}

**Engagement & Behavior:**
- Library Visits/Month: {student_data.get('library_visits_per_month', 0)}
- Activity Participation: {student_data.get('participation_in_activities', 'N/A')}
- Disciplinary Issues: {student_data.get('disciplinary_issues', 'N/A')}
- Counseling Sessions: {student_data.get('counseling_sessions_attended', 0)}
- Class Interaction: {student_data.get('class_interaction', 'N/A')}
- Online Activity: {student_data.get('online_platform_activity', 0):.1f}%
- Peer Study Group: {student_data.get('peer_study_group', 'N/A')}
- Mentor Meetings: {student_data.get('mentor_meetings', 0)}

**External Factors:**
- Commute Distance: {student_data.get('commute_distance', 0):.1f} km
- Part-time Job: {student_data.get('part_time_job', 'N/A')}
- Family Education: {student_data.get('family_education_background', 'N/A')}
- Health Issues: {student_data.get('health_issues', 'N/A')}

**Task:**
Analyze this student's data and assess their attrition risk. Predict:
- **Low Risk**: Student is doing well, unlikely to drop out
- **Medium Risk**: Student shows warning signs, needs monitoring and support
- **High Risk**: Student is in danger of dropping out, needs immediate intervention

**Factor Weights:**
- Attendance: 25%
- Academic Performance: 25%
- Previous Academic Record: 20%
- Backlogs: 15%
- Financial Status: 10%
- Engagement: 5%

**Return ONLY valid JSON (no markdown, no code blocks):**
{{
    "risk_category": "Low Risk/Medium Risk/High Risk",
    "confidence": 85.5,
    "attrition_probability": 35.5,
    "retention_priority": "Low/High/Immediate",
    "critical_risk_factors": [
        "Most critical factor 1",
        "Most critical factor 2",
        "Most critical factor 3"
    ],
    "protective_factors": [
        "Positive factor 1",
        "Positive factor 2"
    ],
    "retention_strategies": [
        "Specific actionable strategy 1",
        "Specific actionable strategy 2",
        "Specific actionable strategy 3",
        "Specific actionable strategy 4"
    ],
    "immediate_actions": [
        "Urgent action 1",
        "Urgent action 2"
    ],
    "long_term_interventions": [
        "Long-term intervention 1",
        "Long-term intervention 2"
    ],
    "recommended_support": {{
        "academic": "Academic support recommendation",
        "financial": "Financial support recommendation",
        "counseling": "Counseling recommendation",
        "mentoring": "Mentoring recommendation"
    }},
    "timeline": "Immediate/Within 1 week/Within 1 month",
    "analysis": "2-3 sentence comprehensive analysis explaining the risk assessment"
}}

**Important:** Base your assessment on the weighted factors. Be specific and actionable in all recommendations.
"""
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean response
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # Extract JSON
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response_text)
        
        return result
        
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return {
            "risk_category": "Medium Risk",
            "confidence": 50.0,
            "attrition_probability": 50.0,
            "retention_priority": "High",
            "critical_risk_factors": ["Unable to analyze - API error"],
            "protective_factors": ["N/A"],
            "retention_strategies": ["Please try again"],
            "immediate_actions": ["Contact system administrator"],
            "long_term_interventions": ["N/A"],
            "recommended_support": {
                "academic": "N/A",
                "financial": "N/A",
                "counseling": "N/A",
                "mentoring": "N/A"
            },
            "timeline": "Immediate",
            "analysis": f"Error: {str(e)}"
        }

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        success, result = login_user(username, password)
        
        if success:
            session['user'] = result
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': result})
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        institution = data.get('institution')
        department = data.get('department')
        
        success, result = register_user(username, email, password, full_name, institution, department)
        
        return jsonify({'success': success, 'message': result})
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/students')
def get_students():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if df_students is None:
        return jsonify({'error': 'No student data available'}), 404
    
    students = df_students[['student_id', 'name', 'program', 'semester', 'risk_category', 'retention_priority']].to_dict('records')
    return jsonify(students)

@app.route('/api/assess', methods=['POST'])
def assess():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    student_id = data.get('student_id')
    
    if df_students is None:
        return jsonify({'error': 'No student data available'}), 404
    
    # Get student data
    student = df_students[df_students['student_id'] == student_id]
    
    if student.empty:
        return jsonify({'error': 'Student not found'}), 404
    
    student_data = student.iloc[0].to_dict()
    
    # Analyze with AI
    result = analyze_attrition_risk_with_ai(student_data)
    
    # Log assessment
    log_assessment(
        session['user']['username'],
        student_id,
        result['risk_category'],
        result['confidence']
    )
    
    # Add student info to result
    result['student_id'] = student_data['student_id']
    result['student_name'] = student_data['name']
    result['program'] = student_data['program']
    result['semester'] = student_data['semester']
    result['attendance'] = student_data['attendance_percentage']
    result['avg_internal'] = (student_data['internal_marks_1'] + student_data['internal_marks_2'] + student_data['internal_marks_3']) / 3
    result['cgpa'] = student_data['previous_semester_cgpa']
    result['backlogs'] = student_data['backlogs']
    result['fee_status'] = student_data['fee_payment_status']
    
    return jsonify(result)

@app.route('/api/assess-custom', methods=['POST'])
def assess_custom():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Analyze with AI
    result = analyze_attrition_risk_with_ai(data)
    
    # Log assessment
    log_assessment(
        session['user']['username'],
        'CUSTOM',
        result['risk_category'],
        result['confidence']
    )
    
    return jsonify(result)

@app.route('/api/stats')
def get_stats():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if df_students is None:
        return jsonify({'error': 'No student data available'}), 404
    
    stats = {
        'total_students': len(df_students),
        'low_risk': len(df_students[df_students['risk_category'] == 'Low Risk']),
        'medium_risk': len(df_students[df_students['risk_category'] == 'Medium Risk']),
        'high_risk': len(df_students[df_students['risk_category'] == 'High Risk']),
        'avg_attendance': float(df_students['attendance_percentage'].mean()),
        'avg_cgpa': float(df_students['previous_semester_cgpa'].mean()),
        'students_with_backlogs': len(df_students[df_students['backlogs'] > 0]),
        'fee_defaulters': len(df_students[df_students['fee_payment_status'].isin(['Defaulted', 'Pending'])])
    }

    return jsonify(stats)
    

if __name__ == '__main__':
    # Generate data if it doesn't exist
    if not os.path.exists('student_attrition_data.csv'):
        print("Generating student data...")
        from generate_data import generate_attrition_data
        generate_attrition_data(500)
    
    app.run(debug=True, port=5000)