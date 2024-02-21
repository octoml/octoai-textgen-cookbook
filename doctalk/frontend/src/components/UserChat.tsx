"use client";

import { FormEvent, Fragment, useState } from "react";
import LoadingDots from "./LoadingDots";
import ErrorBanner from "./ErrorBanner";
import Prompt from "./Prompt";
import ChatBubble from "./ChatBubble";

interface MessageProps {
  question: string;
  answer: string;
}

const UserChat = () => {
  const initialPrompt = "What is a vector database?";
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState<MessageProps[]>([]);
  const [error, setError] = useState(false);
  const [questionSubmitted, setQuestionSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setQuestionSubmitted(true);

    const response = await fetch("/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: inputValue || initialPrompt,
      }),
    });

    if (!response.ok) {
      setError(true);
    } else {
      setLoading(false);
      setError(false);
    }

    const chatAnswer = await response.json();

    // set messages array to include latest question + answer
    setMessages([
      ...messages,
      {
        question: inputValue || initialPrompt,
        answer: chatAnswer.message_llm1,
      },
    ]);
  };

  return (
    <div className={`interactive ${questionSubmitted ? "condensed" : ""}`}>
      <Prompt
        formLabel="Go for it, ask a question"
        btnText="See response"
        size={questionSubmitted ? "sm" : "lg"}
        initialPrompt={initialPrompt}
        inputValue={inputValue}
        setInputValue={setInputValue}
        handleSubmit={handleSubmit}
        loading={loading}
      />
      <div className="result chat">
        {loading && <LoadingDots />}
        {messages.length > 0 &&
          // display most recent messages first
          messages
            .slice()
            .reverse()
            .map((message, index) => (
              <Fragment key={message.question + index}>
                <ChatBubble key={message.question} text={message.question} />
                <ChatBubble
                  key={message.answer}
                  text={message.answer}
                  color="secondary"
                />
              </Fragment>
            ))}
      </div>
      {error && (
        <ErrorBanner bannerText="There was an error generating the answer, please try again." />
      )}
    </div>
  );
};

export default UserChat;
