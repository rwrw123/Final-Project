function feedback(input) {
    if (input.length < 5) {
        return { message: 'Input is too short.', isValid: false };
    }
    return { message: 'Looks good!', isValid: true };
}

export default feedback;
