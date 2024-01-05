import axios from 'axios';

export const sendQuestion = async (question: string) => {
    const maxTokens = 512;
    const response = await axios.post(
        `${process.env.OCTO_LLAMA_DOMAIN}/chat/completions`,
        {
            model: 'llama-2-7b-chat',
            messages: [
                {
                    role: 'system',
                    content: `Below is an instruction that describes a task. Write a response that appropriately completes the request within ${maxTokens} words.`
                },
                {
                    role: 'user',
                    content: question
                }
            ],
            stream: false,
            max_tokens: maxTokens
        },
        {
            headers: {
                'Content-type': 'application/json',
                'X-OctoAI-Async': '1',
                Authorization: `Bearer ${process.env.OCTO_TOKEN}`
            }
        }
    );
    const { response_id, poll_url: _pollUrl } = response.data;

    return response_id;
};

export const pollResponse = async (pollId: string) => {
    const pollResponseFn = await axios.get(
        `${process.env.OCTO_ASYNC_DOMAIN}/requests/${pollId}`,
        {
            headers: {
                'Content-type': 'application/json',
                'X-OctoAI-Async': '1',
                Authorization: `Bearer ${process.env.OCTO_TOKEN}`
            }
        }
    );

    return pollResponseFn.data;
};

export const getAnswer = async (pollId: string) => {
    const completedResponse = await axios.get(
        `${process.env.OCTO_ASYNC_DOMAIN}/responses/${pollId}`,
        {
            headers: {
                'Content-type': 'application/json',
                'X-OctoAI-Async': '1',
                Authorization: `Bearer ${process.env.OCTO_TOKEN}`
            }
        }
    );
    const { choices } = completedResponse.data;
    const answer = choices[0].message.content;

    return answer;
};
