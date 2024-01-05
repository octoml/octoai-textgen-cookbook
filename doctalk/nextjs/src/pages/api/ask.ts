import type { NextApiRequest, NextApiResponse } from 'next';

import { sendQuestion } from '@/utils/llama';

type ResponseData = {
    questionId: string;
};

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<ResponseData>
) {
    const response = await sendQuestion(req.body.question);
    res.status(200).json({ questionId: response });
}
