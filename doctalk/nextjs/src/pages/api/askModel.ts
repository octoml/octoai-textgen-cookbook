import type { NextApiRequest, NextApiResponse } from 'next';

import { getAnswers } from '@/utils/api';

type ResponseData = {
    message: string;
    error?: any;
};

export const config = {
    maxDuration: 60
};

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<ResponseData>
) {
    const { question, dataSource } = req.body;
    const response = await getAnswers(question, dataSource);
    if (response.error) {
        res.status(500).json({
            message: 'There was a problem',
            error: response.error
        });
    } else {
        res.status(200).json({ ...response });
    }
}
