from flask import Flask, jsonify, request, abort, render_template

app = Flask(__name__)


doctors = [
    {"id": 1, "name": "Dr. Manu", "location": "Government Hospital", "availability": "Evenings", "max_patients": 5, "schedule": {"Monday": "Available", "Tuesday": "Available", "Wednesday": "Not Available", "Thursday": "Available", "Friday": "Not Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 2, "name": "Dr. Anand", "location": "City Hospital", "availability": "Evenings", "max_patients": 15, "schedule": {"Monday": "Available", "Tuesday": "Available", "Wednesday": "Available", "Thursday": "Available", "Friday": "Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 3, "name": "Dr. Anshu", "location": "Private Hospital", "availability": "Evenings", "max_patients": 10, "schedule": {"Monday": "Not Available", "Tuesday": "Available", "Wednesday": "Available", "Thursday": "Not Available", "Friday": "Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 4, "name": "Dr. Ayush", "location": "Private Hospital", "availability": "Evenings", "max_patients": 25, "schedule": {"Monday": "Available", "Tuesday": "Available", "Wednesday": "Available", "Thursday": "Available", "Friday": "Not Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 5, "name": "Dr. Gaurav", "location": "Private Hospital", "availability": "Evenings", "max_patients": 12, "schedule": {"Monday": "Available", "Tuesday": "Not Available", "Wednesday": "Available", "Thursday": "Available", "Friday": "Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 6, "name": "Dr. Mayur", "location": "City Hospital", "availability": "Evenings", "max_patients": 10, "schedule": {"Monday": "Available", "Tuesday": "Available", "Wednesday": "Not Available", "Thursday": "Available", "Friday": "Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 7, "name": "Dr. Amrish", "location": "Government Hospital", "availability": "Evenings", "max_patients": 20, "schedule": {"Monday": "Available", "Tuesday": "Available", "Wednesday": "Available", "Thursday": "Available", "Friday": "Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 8, "name": "Dr. Bhagat", "location": "City Hospital", "availability": "Evenings", "max_patients": 16, "schedule": {"Monday": "Not Available", "Tuesday": "Available", "Wednesday": "Not Available", "Thursday": "Not Available", "Friday": "Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 9, "name": "Dr. Manish", "location": "Government Hospital", "availability": "Evenings", "max_patients": 15, "schedule": {"Monday": "Available", "Tuesday": "Not Available", "Wednesday": "Available", "Thursday": "Not Available", "Friday": "Available", "Saturday": "Available", "Sunday": "Not Available"}},
    {"id": 10, "name": "Dr. Aakriti", "location": "Government Hospital", "availability": "Evenings", "max_patients": 21, "schedule": {"Monday": "Available", "Tuesday": "Available", "Wednesday": "Available", "Thursday": "Available", "Friday": "Available", "Saturday": "Not Available", "Sunday": "Not Available"}},
]
booked_appointments = {}

@app.route('/')
def index():
    return render_template('index.html')

#Doctor list
@app.route('/doctors', methods=['GET'])
def get_doctors():
    return render_template('doctors_list.html',doctors=doctors)

# doctor list with appointment
@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = next((doc for doc in doctors if doc['id'] == doctor_id), None)
    if doctor is None:
        abort(404, "Doctor not found")
    appointments_booked = booked_appointments.get(doctor_id, 0)

    doctor_with_appointments = {
        "id": doctor['id'],
        "name": doctor['name'],
        "location": doctor['location'],
        "availability": doctor['availability'],
        "max_patients": doctor['max_patients'],
        "schedule": doctor['schedule'],
        "appointments_booked": appointments_booked
    }

    return render_template('doctor_appointments.html', doctor=doctor_with_appointments)

# to book appointment
@app.route('/appointments/book', methods=['GET', 'POST'])
def book_appointment():

    if request.method == 'POST':
        data = request.form  
        doctor_id = int(data.get('doctor_id'))
        day = data.get('day')

        if doctors[doctor_id - 1]['schedule'].get(day) != "Available":
            result_messages = "Doctor not available on the selected day"
            return render_template('book_appointment.html', doctors=doctors, result_messages=result_messages)

        max_patients = doctors[doctor_id - 1]['max_patients']
        appointments_booked = booked_appointments.get(doctor_id, 0)

        if appointments_booked < max_patients:
            booked_appointments[doctor_id] = appointments_booked + 1
            result_message = "Appointment booked successfully"
        else:
            result_message = "Maximum number of patients reached"
        return render_template('book_appointment.html', doctors=doctors, result_message=result_message)
        
    else:
        return render_template('book_appointment.html', doctors=doctors)


if __name__ == '__main__':
    app.run(debug=False)
