import Input from './Input';
import Model from './Model/Model';
import Responses from './Responses/Responses';
import UserQuestion from './UserQuestion';

const EntryPoint = () => (
    <div className='flex flex-col gap-12 xl:gap-14'>
        <UserQuestion />
        <Model />
        <Responses />
        <Input />
    </div>
);

export default EntryPoint;
