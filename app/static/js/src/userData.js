async function fetchUserData(userId) {
    const response = await fetch(`http://localhost:5000/api/users/${userId}`);
    return await response.json();
}

module.exports = { fetchUserData };

