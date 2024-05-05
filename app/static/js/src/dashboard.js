import React, { useEffect, useState } from 'react';
import fetchUserData from './userData';

function Dashboard({ userId }) {
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchUserData(userId)
            .then(data => setUserData(data))
            .catch(err => setError(err.message));
    }, [userId]);

    if (error) {
        return <p>Error: {error}</p>;
    }

    if (!userData) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h2>Welcome, {userData.name}!</h2>
            <p>Your health records:</p>
            <ul>
                {userData.records.map(record => (
                    <li key={record.id}>
                        Date: {record.date}, Temperature: {record.temperature}, Blood Pressure: {record.blood_pressure}, Heart Rate: {record.heart_rate}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Dashboard;
