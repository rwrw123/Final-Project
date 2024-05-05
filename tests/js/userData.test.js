const fetchUserData = require('./userData');

// Mocking fetch globally
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ id: 1, name: 'Zoe Doe' }),
    ok: true
  })
);

beforeEach(() => {
  fetch.mockClear();
});

test('fetches user data', async () => {
    const data = await fetchUserData(1);
    expect(data.name).toBe('Zoe Doe');
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/users/1');
});
