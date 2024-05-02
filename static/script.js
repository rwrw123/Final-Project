document.getElementById('addUserForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    axios.post('/users/add', {
        name: formData.get('name'),
        email: formData.get('email')
    }).then(function(response) {
        alert('User added successfully!');
    }).catch(function(error) {
        alert('Failed to add user: ' + error.response.data.error);
    });
});

document.getElementById('registerDeviceForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    axios.post('/devices/register', {
        deviceId: formData.get('deviceId'),
        type: formData.get('type')
    }).then(function(response) {
        alert('Device registered successfully!');
    }).catch(function(error) {
        alert('Failed to register device: ' + error.response.data.error);
    });
});

document.getElementById('submitMeasurementForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    axios.post(`/patients/${formData.get('patientId')}/measurements/add`, {
        type: formData.get('type'),
        value: formData.get('value')
    }).then(function(response) {
        alert('Measurement submitted successfully!');
    }).catch(function(error) {
        alert('Failed to submit measurement: ' + error.response.data.error);
    });
});

document.getElementById('bookAppointmentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    axios.post(`/patients/${formData.get('patientId')}/appointments/book`, {
        mpId: formData.get('mpId'),
        time: formData.get('time')
    }).then(function(response) {
        alert('Appointment booked successfully!');
    }).catch(function(error) {
        alert('Failed to book appointment: ' + error.response.data.error);
    });
});

document.getElementById('sendMessageForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    axios.post(`/chat/${formData.get('patientId')}`, {
        content: formData.get('content')
    }).then(function(response) {
        alert('Message sent successfully!');
    }).catch(function(error) {
        alert('Failed to send message: ' + error.response.data.error);
    });
});
