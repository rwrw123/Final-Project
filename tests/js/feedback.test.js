const feedback = require('../../app/static/js/src/feedback.js');

describe('feedback for user input', () => {
    test('returns error for short input', () => {
        const result = feedback('Hi');
        expect(result).toBe('Input too short');
    });

    test('returns success for valid input', () => {
        const result = feedback('Hello, world!');
        expect(result).toBe('Valid input');
    });
});


