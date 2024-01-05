import { ZuSlice } from '../../declarations';

export interface LoadingSlice {
    loading: boolean;
    setLoading: (arg: LoadingSlice['loading']) => void;
    error: boolean;
    setError: (arg: LoadingSlice['error']) => void;
}

const createLoadingSlice: ZuSlice<LoadingSlice> = (
    set: (arg: () => Partial<LoadingSlice>) => void
) => ({
    loading: false,
    setLoading: (arg) => set(() => ({ loading: arg })),
    error: false,
    setError: (arg) => set(() => ({ error: arg }))
});

export default createLoadingSlice;
