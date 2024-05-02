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


