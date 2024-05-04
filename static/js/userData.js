async function fetchUserData(userId) {
    const response = await fetch(`http://localhost:5000/api/users/${userId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch user data');
    }
    return response.json();
}

module.exports = fetchUserData;
