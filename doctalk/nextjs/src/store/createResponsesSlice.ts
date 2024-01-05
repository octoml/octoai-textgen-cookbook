import { ZuSlice } from '../../declarations';

import { LlamaResponse } from '@/utils/models/llamaResponse';

export interface ResponsesSlice {
    responses: LlamaResponse[];
    setResponses: (arg: LlamaResponse[]) => void;
}

const createQuestionSlice: ZuSlice<ResponsesSlice> = (
    set: (fn: (state: ResponsesSlice) => Partial<ResponsesSlice>) => void
) => ({
    responses: [],
    setResponses: (arg) =>
        set((state) => {
            const updatedResponses = state.responses.slice();

            arg.forEach((newResponse) => {
                const existingResponse = updatedResponses.find(
                    (response) => response.time === newResponse.time
                );

                if (existingResponse) {
                    Object.assign(existingResponse, newResponse);
                } else {
                    updatedResponses.push(newResponse);
                }
            });

            return { responses: updatedResponses };
        })
});

export default createQuestionSlice;
