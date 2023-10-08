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