import { DateTime } from 'luxon';
import { NextApiRequest, NextApiResponse } from 'next';

// import { getAnswer, pollResponse } from '@/shared/utils/llama';
import { getAnswer, pollResponse } from '@/utils/llama';
import { LlamaResponse } from '@/utils/models/llamaResponse';

// const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<{ completed: boolean; response?: LlamaResponse }>
) {
    const { id } = req.query;
    const { body } = req;
    const { question } = body;
    try {
        const pollId = id as string;
        const response = await pollResponse(pollId);
        if (response.status === 'completed') {
            const answer = await getAnswer(pollId);
            res.status(200).json({
                response: {
                    llama: {
                        response: answer,
                        usage: {
                            price: 0,
                            tokens: 0
                        }
                    },
                    question,
                    questionId: pollId,
                    time: DateTime.now()
                },
                completed: true
            });
        } else {
            res.status(200).json({
                completed: false
            });
        }
    } catch (error) {
        const responseError = error as any;
        console.error('Error', responseError.response.data);
    }
}
