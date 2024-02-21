import { Dispatch, FC, FormEvent, SetStateAction } from "react";

interface PromptProps {
  /** Label that displays on top of form */
  formLabel?: string;
  /** Text inside of form button */
  btnText?: string;
  /** Input sizing */
  size?: "sm" | "lg";
  /** Initial prompt, used as a placeholder */
  initialPrompt: string;
  /** User defined prompt */
  inputValue: string;
  /** Set user defined prompt */
  setInputValue: Dispatch<SetStateAction<string>>;
  /** Function that runs on form submit */
  handleSubmit: (e: FormEvent<HTMLFormElement>) => Promise<void> | void;
  /** State of user chat response */
  loading: boolean;
}

const Prompt: FC<PromptProps> = ({
  formLabel = "Enter prompt",
  btnText = "Generate",
  size = "sm",
  initialPrompt,
  inputValue,
  setInputValue,
  handleSubmit,
  loading,
}) => {
  return (
    <form id="prompt" className={size} onSubmit={handleSubmit}>
      <label>
        <p>{formLabel}</p>
        <input
          id="input-prompt"
          type="text"
          placeholder={initialPrompt}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
      </label>
      <button id="generate-btn" disabled={loading}>
        {btnText}
      </button>
    </form>
  );
};

export default Prompt;
