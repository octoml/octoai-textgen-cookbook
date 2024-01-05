import { create } from 'zustand';

import createDataSourceSlice, {
    DataSourceSlice
} from '@/store/createDataSourceSlice';
import createLoadingSlice, { LoadingSlice } from '@/store/createLoadingSlice';
import createQuestionSlice, {
    QuestionSlice
} from '@/store/createQuestionSlice';
import createResponsesSlice, {
    ResponsesSlice
} from '@/store/createResponsesSlice';

type StoreState = QuestionSlice &
    ResponsesSlice &
    LoadingSlice &
    DataSourceSlice;

const useStore = create<StoreState>()((...args) => ({
    ...createQuestionSlice(...args),
    ...createResponsesSlice(...args),
    ...createLoadingSlice(...args),
    ...createDataSourceSlice(...args)
}));

export default useStore;
