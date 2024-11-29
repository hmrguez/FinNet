// thesis-web/src/App.tsx
import './App.css'
import TextInput from "./components/TextInput.tsx";
import {useEffect, useState} from "react";
import Chat from "./components/Chat.tsx";
import { respond } from "./services/respond.service.ts";

function App() {
    const [value, setValue] = useState<string>("")
    const [messages, setMessages] = useState([
        { id: '1', text: 'Hello!', mine: true },
        { id: '2', text: 'Hi there!', mine: false },
    ]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [darkMode, setDarkMode] = useState<boolean>(false);

    useEffect(() => {
        if (darkMode) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [darkMode]);

    const handleSend = () => {
        if (value.trim() === "") return;

        const newMessage = { id: (messages.length + 1).toString(), text: value, mine: true };
        setMessages([...messages, newMessage]);
        setValue("");
        setIsLoading(true);

        setTimeout(() => {
            const response = respond(value);
            const responseMessage = { id: Math.random().toString(36).substr(2, 9), text: response, mine: false };
            setMessages(prevMessages => [...prevMessages, responseMessage]);
            setIsLoading(false);
        }, 1000); // Simulate response delay
    };

    return (
        <div className={`p-10 ${darkMode ? 'dark' : ''}`}>
            <button
                onClick={() => setDarkMode(!darkMode)}
                className="dark:bg-gray-600 mb-4 p-2 bg-gray-200  rounded"
            >
                Toggle Dark Mode
            </button>
            <Chat initialMessages={messages} isLoading={isLoading}/>
            <TextInput value={value} onChange={setValue} onSend={handleSend}/>
        </div>
    )
}

export default App;