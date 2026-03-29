import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def text_to_pdf(text, output_file):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Create PDF document
    doc = SimpleDocTemplate(output_file)

    # Get styles
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    # Split text into paragraphs (by line breaks)
    lines = text.split("\n")

    # Create flowable elements
    content = []
    for line in lines:
        content.append(Paragraph(line, style))
        content.append(Spacer(1, 10))

    # Build PDF
    doc.build(content)

# ---- YOUR INPUT TEXT HERE ----
my_text = """Company Policy Document
Page 1: Introduction to Company Policy

1.1 Purpose of Company Policy

The purpose of this Company Policy document is to provide employees with a clear understanding of the expectations, values, and rules that guide our company’s operations. These policies apply to all employees and are designed to ensure a productive, respectful, and legally compliant work environment.

1.2 Scope of Policies

These policies apply to all full-time, part-time, and temporary employees across all departments and locations within the company. Employees must familiarize themselves with and adhere to these policies as part of their employment responsibilities.

Page 2: Code of Conduct

2.1 General Behavior Expectations

Employees are expected to conduct themselves in a professional manner at all times. This includes treating colleagues, customers, and clients with respect and courtesy. Discriminatory, harassing, or inappropriate behavior will not be tolerated under any circumstances.

2.2 Integrity and Honesty

Integrity is a core value of our company. Employees must be truthful in all business dealings, and any form of dishonesty or fraud will result in disciplinary action, up to and including termination.

2.3 Confidentiality

Employees must maintain confidentiality of all proprietary and sensitive company information. This includes intellectual property, financial data, customer details, and any other confidential materials that could harm the company if disclosed.

Page 3: Workplace Safety and Health

3.1 Health and Safety Protocols

The company is committed to maintaining a safe and healthy work environment. All employees must follow safety procedures and report any hazards, accidents, or injuries to their supervisors immediately. Safety guidelines are provided during orientation and updated regularly.

3.2 Emergency Procedures

In case of emergencies such as fires, earthquakes, or medical crises, employees must follow the emergency response procedures outlined in the employee handbook. These procedures are also posted in key areas around the workplace.

3.3 Substance Abuse

The use of illegal drugs, alcohol, or any other substances that impair an employee's ability to perform their duties is strictly prohibited. Employees found violating this policy may face disciplinary actions, including suspension or termination.

Page 4: Attendance and Punctuality

4.1 Work Hours

Employees are expected to adhere to their designated work hours. Any changes to this schedule, including overtime, must be pre-approved by management. If an employee needs time off, they are required to submit a request through the proper channels.

4.2 Absences and Lateness

Employees must notify their supervisors as early as possible if they are unable to attend work. Excessive absenteeism or tardiness will be subject to disciplinary measures, including verbal or written warnings.

4.3 Leave of Absence

Employees are entitled to various forms of leave, including vacation, sick leave, and parental leave, in accordance with company policy and applicable laws. Requests for extended leaves of absence should be submitted in advance.

Page 5: Employee Benefits and Compensation

5.1 Salary and Wages

Employees will be compensated fairly based on their job position, qualifications, and performance. Salaries are reviewed annually and adjustments are made in accordance with the company’s budget and market conditions.

5.2 Health Insurance

The company provides health insurance benefits to full-time employees. Coverage options include medical, dental, and vision plans. Employees can enroll in these benefits during the open enrollment period or upon hire.

5.3 Retirement Plan

The company offers a retirement plan that includes employer contributions. Employees are encouraged to participate and plan for their future through this retirement savings program."""

# ---- OUTPUT FILE NAME ----
output_path = os.path.join("data", "policy.pdf")

# Run function
text_to_pdf(my_text, output_path)

print("PDF created successfully!")