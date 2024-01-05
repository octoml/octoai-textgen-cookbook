import { DateTime } from 'luxon';

export interface modelResponse {
    response: string;
    usage: {
        price: number;
        tokens: number;
    };
}

export interface LlamaResponse {
    questionId: string;
    question: string;
    llama: modelResponse;
    time: DateTime;
}
