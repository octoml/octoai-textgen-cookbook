import { FC } from "react";
import Markdown from 'react-markdown'

interface ChatBubbleProps {
  /** Chat bubble text */
  text: string;
  /** Chat bubble color */
  color?: "primary" | "secondary";
}

const ChatBubble: FC<ChatBubbleProps> = ({ text, color = "primary" }) => {
  // remove default string prefix
  const formattedText = text.replace("#LLAMA-2#\n", "")

  return (
    <div className={`chat-bubble ${color}`}>
      <Markdown>{formattedText}</Markdown>
    </div>
  )
};

export default ChatBubble;
