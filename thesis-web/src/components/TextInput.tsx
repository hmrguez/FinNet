// thesis-web/src/components/TextInput.tsx
import {MessageCircleCodeIcon} from 'lucide-react'

interface TextInputProps {
    value: string;
    onChange: (value: string) => void;
    onSend: () => void;
}

const TextInput = (props: TextInputProps) => {
    const {value, onChange, onSend} = props;

    return (
        <div className="flex justify-center fixed bottom-[10%] right-[50%]">
            <input
                className="bg-gray-100 dark:bg-gray-700 rounded-2xl p-2 px-8 fixed w-5/6 mx-auto focus:outline-none focus:ring-2 focus:ring-purple-300 dark:focus:ring-thicker-purple"
                placeholder={"Enter message"}
                type="text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
            />
            <MessageCircleCodeIcon
                onClick={onSend}
                className="fixed text-gray-400 dark:text-gray-300 right-[15%] bottom-[6.3%] hover:cursor-pointer"
            />
        </div>
    );
}

export default TextInput;