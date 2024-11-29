// thesis-web/src/components/Chat.tsx
import {useEffect, useState} from "react";

interface Message {
    id: string;
    text: string;
    mine: boolean;
}

interface ChatProps {
    initialMessages: Message[];
    isLoading: boolean;
}

const Chat = ({initialMessages, isLoading}: ChatProps) => {
    const [messages, setMessages] = useState<Message[]>([]);

    useEffect(() => {
        setMessages(initialMessages);
    }, [initialMessages]);

    return (
        <div className="flex flex-col p-4 dark:bg-gray-800">
            {messages.map((message) => (
                <div
                    key={message.id}
                    className={`p-2 px-4 my-2 rounded-xl message-enter-active drop-shadow-md w-fit message-enter ${
                        message.mine ? 'bg-purple-400 dark:bg-thicker-purple text-white self-end' : 'bg-white dark:bg-gray-700 text-black dark:text-white self-start'
                    }`}
                >
                    {message.text}
                </div>
            ))}
            {isLoading && (
                <div className="p-2 px-4 my-2 rounded-xl drop-shadow-md w-fit bg-white dark:bg-gray-700 text-black dark:text-white self-start placeholder">
                    <span>.</span><span>.</span><span>.</span>
                </div>
            )}
        </div>
    )
}

export default Chat;