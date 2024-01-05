import { ZuSlice } from '../../declarations';

export interface DataSourceSlice {
    dataSource: string;
    setDataSource: (arg: DataSourceSlice['dataSource']) => void;
    userChangedData: boolean;
    setUserChangedData: (arg: DataSourceSlice['userChangedData']) => void;
}

const createDataSourceSlice: ZuSlice<DataSourceSlice> = (
    set: (arg: () => Partial<DataSourceSlice>) => void
) => ({
    dataSource: 'octoai_docs',
    setDataSource: (arg) => set(() => ({ dataSource: arg })),
    userChangedData: false,
    setUserChangedData: (arg) => set(() => ({ userChangedData: arg }))
});

export default createDataSourceSlice;
