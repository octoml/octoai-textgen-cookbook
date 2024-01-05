import { ZuSlice } from '../../declarations';

export interface QuestionSlice {
    question: string;
    setQuestion: (arg: QuestionSlice['question']) => void;
    fullQuestion: string;
    setFullQuestion: (arg: QuestionSlice['fullQuestion']) => void;
}

const createQuestionSlice: ZuSlice<QuestionSlice> = (
    set: (arg: () => Partial<QuestionSlice>) => void
) => ({
    question: '',
    setQuestion: (arg) => set(() => ({ question: arg })),
    fullQuestion: '',
    setFullQuestion: (arg) => set(() => ({ fullQuestion: arg }))
});

export default createQuestionSlice;
