function feedback(input) {
    if (input.length < 5) {
        return 'Input too short';
    }
    return 'Valid input';
}

module.exports = feedback;
