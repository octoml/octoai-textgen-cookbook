'use client';

import useStore from '@/store/useStore';

const UserQuestion = () => {
    const { fullQuestion } = useStore();

    return (
        <>
            {fullQuestion && (
                <div className='m-auto  flex gap-8'>
                    <div className='flex flex-col items-center justify-center gap-1'>
                        <p className='text-xl font-normal'>You asked:</p>
                        <p className='text-center text-3xl leading-9 md:text-5xl'>
                            {fullQuestion}
                        </p>
                    </div>
                </div>
            )}
        </>
    );
};

export default UserQuestion;
