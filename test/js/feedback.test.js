const feedback = require('./feedback');

describe('feedback for user input', () => {
    test('returns error for short input', () => {
        expect(feedback('123').isValid).toBe(false);
        expect(feedback('123').message).toMatch(/too short/);
    });

    test('approves valid input', () => {
        expect(feedback('12345').isValid).toBe(true);
        expect(feedback('12345').message).toMatch(/Looks good!/);
    });
});
