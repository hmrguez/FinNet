
export const respond = (message: string): string => {
    // Simple response logic based on the message
    if (message.toLowerCase().includes("hello")) {
        return "Hi there!";
    } else if (message.toLowerCase().includes("how are you")) {
        return "I'm good, thanks!";
    } else {
        return "I don't understand.";
    }
};