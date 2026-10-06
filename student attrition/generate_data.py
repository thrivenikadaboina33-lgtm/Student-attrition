import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_attrition_data(num_students=500):
    """Generate synthetic student attrition data"""
    
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    # Programs and departments
    programs = ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'IT', 'Business Administration']
    departments = ['Engineering', 'Management', 'Science', 'Arts']
    semesters = [1, 2, 3, 4, 5, 6, 7, 8]
    
    for i in range(num_students):
        # Basic info
        student_id = f"STU{2024000 + i}"
        name = f"Student_{i+1}"
        age = random.randint(18, 24)
        gender = random.choice(['Male', 'Female'])
        program = random.choice(programs)
        department = random.choice(departments)
        semester = random.choice(semesters)
        
        # Academic performance
        attendance_percentage = round(random.uniform(35, 100), 2)
        internal_marks_1 = round(random.uniform(20, 100), 2)
        internal_marks_2 = round(random.uniform(20, 100), 2)
        internal_marks_3 = round(random.uniform(20, 100), 2)
        assignment_score = round(random.uniform(25, 100), 2)
        project_score = round(random.uniform(30, 100), 2)
        
        # Previous academic records
        previous_semester_cgpa = round(random.uniform(4.0, 10.0), 2)
        previous_year_percentage = round(random.uniform(40, 95), 2)
        backlogs = random.randint(0, 8)
        
        # Financial factors
        fee_payment_status = random.choice(['Paid', 'Pending', 'Partial', 'Defaulted'])
        scholarship = random.choice(['Yes', 'No'])
        financial_difficulty = random.choice(['Low', 'Medium', 'High'])
        
        # Behavioral factors
        library_visits_per_month = random.randint(0, 20)
        participation_in_activities = random.choice(['Low', 'Medium', 'High'])
        disciplinary_issues = random.choice(['None', 'Minor', 'Major'])
        counseling_sessions_attended = random.randint(0, 10)
        
        # Engagement metrics
        class_interaction = random.choice(['Low', 'Medium', 'High'])
        online_platform_activity = round(random.uniform(0, 100), 2)  # percentage
        peer_study_group = random.choice(['Yes', 'No'])
        mentor_meetings = random.randint(0, 15)
        
        # External factors
        commute_distance = round(random.uniform(5, 80), 1)  # km
        part_time_job = random.choice(['Yes', 'No'])
        family_education_background = random.choice(['Graduate', 'Undergraduate', 'School', 'None'])
        health_issues = random.choice(['None', 'Minor', 'Major'])
        
        # Calculate attrition risk score
        risk_score = 0
        
        # Attendance impact (25%)
        if attendance_percentage < 50:
            risk_score += 25
        elif attendance_percentage < 65:
            risk_score += 18
        elif attendance_percentage < 75:
            risk_score += 10
        
        # Academic performance impact (25%)
        avg_internal = (internal_marks_1 + internal_marks_2 + internal_marks_3) / 3
        if avg_internal < 40:
            risk_score += 25
        elif avg_internal < 50:
            risk_score += 18
        elif avg_internal < 60:
            risk_score += 10
        
        # Previous academic record impact (20%)
        if previous_semester_cgpa < 5.0:
            risk_score += 20
        elif previous_semester_cgpa < 6.0:
            risk_score += 15
        elif previous_semester_cgpa < 7.0:
            risk_score += 8
        
        # Backlogs impact (15%)
        if backlogs >= 5:
            risk_score += 15
        elif backlogs >= 3:
            risk_score += 10
        elif backlogs >= 1:
            risk_score += 5
        
        # Financial factors (10%)
        if fee_payment_status == 'Defaulted':
            risk_score += 10
        elif fee_payment_status == 'Pending':
            risk_score += 7
        elif fee_payment_status == 'Partial':
            risk_score += 4
        
        # Engagement factors (5%)
        if library_visits_per_month < 3:
            risk_score += 3
        if participation_in_activities == 'Low':
            risk_score += 2
        if class_interaction == 'Low':
            risk_score += 3
        if counseling_sessions_attended == 0:
            risk_score += 2
        
        # Additional risk factors
        if disciplinary_issues == 'Major':
            risk_score += 5
        elif disciplinary_issues == 'Minor':
            risk_score += 2
        
        if financial_difficulty == 'High':
            risk_score += 4
        elif financial_difficulty == 'Medium':
            risk_score += 2
        
        if health_issues == 'Major':
            risk_score += 3
        
        if part_time_job == 'Yes' and attendance_percentage < 70:
            risk_score += 3
        
        # Determine risk category and attrition status
        if risk_score >= 70:
            risk_category = 'High Risk'
            attrition_status = 'Likely to Drop Out'
            retention_priority = 'Immediate'
        elif risk_score >= 45:
            risk_category = 'Medium Risk'
            attrition_status = 'At Risk'
            retention_priority = 'High'
        else:
            risk_category = 'Low Risk'
            attrition_status = 'Safe'
            retention_priority = 'Low'
        
        data.append({
            'student_id': student_id,
            'name': name,
            'age': age,
            'gender': gender,
            'program': program,
            'department': department,
            'semester': semester,
            'attendance_percentage': attendance_percentage,
            'internal_marks_1': internal_marks_1,
            'internal_marks_2': internal_marks_2,
            'internal_marks_3': internal_marks_3,
            'assignment_score': assignment_score,
            'project_score': project_score,
            'previous_semester_cgpa': previous_semester_cgpa,
            'previous_year_percentage': previous_year_percentage,
            'backlogs': backlogs,
            'fee_payment_status': fee_payment_status,
            'scholarship': scholarship,
            'financial_difficulty': financial_difficulty,
            'library_visits_per_month': library_visits_per_month,
            'participation_in_activities': participation_in_activities,
            'disciplinary_issues': disciplinary_issues,
            'counseling_sessions_attended': counseling_sessions_attended,
            'class_interaction': class_interaction,
            'online_platform_activity': online_platform_activity,
            'peer_study_group': peer_study_group,
            'mentor_meetings': mentor_meetings,
            'commute_distance': commute_distance,
            'part_time_job': part_time_job,
            'family_education_background': family_education_background,
            'health_issues': health_issues,
            'risk_score': risk_score,
            'risk_category': risk_category,
            'attrition_status': attrition_status,
            'retention_priority': retention_priority
        })
    
    df = pd.DataFrame(data)
    df.to_csv('student_attrition_data.csv', index=False)
    
    print(f"✓ Generated {num_students} student records")
    print(f"\nRisk Distribution:")
    print(df['risk_category'].value_counts())
    print(f"\nAttrition Status:")
    print(df['attrition_status'].value_counts())
    
    return df

if __name__ == "__main__":
    generate_attrition_data(500)