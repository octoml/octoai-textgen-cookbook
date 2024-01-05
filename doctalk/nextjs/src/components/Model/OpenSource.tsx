'use client';

import useStore from '@/store/useStore';

const OpenSource = () => {
    const { fullQuestion } = useStore();

    const textClasses = `${
        fullQuestion ? 'text-sm' : 'text-lg desktop-xl:text-xl'
    } text-gray-100 transition-font`;

    return (
        <div
            className={`inline-block rounded-lg bg-white bg-opacity-5  ${
                fullQuestion ? 'px-4 py-1' : 'px-5 py-2'
            } text-center shadow-border backdrop-blur-3xl`}
        >
            <span className={textClasses}>Open Source</span>
        </div>
    );
};

export default OpenSource;
