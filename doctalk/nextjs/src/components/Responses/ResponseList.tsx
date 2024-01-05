'use client';

import MDEditor from '@uiw/react-md-editor';
import { ThreeDots } from 'react-loader-spinner';

import ResponseCard from './ResponseCard';

import useStore from '@/store/useStore';
import { modelResponse } from '@/utils/models/llamaResponse';

const ResponseList = () => {
    const { responses, fullQuestion, loading } = useStore();

    const formattedResponse = (response: modelResponse) => {
        const parsedText =
            response && response?.response?.split('\n\nResponse ')[0];

        return <MDEditor.Markdown className='markdown' source={parsedText} />;
    };

    const responseTime = (response: modelResponse) => {
        const secondsString =
            response &&
            response?.response?.split('\n\nResponse ')[1].replace(/\(|\)/g, '');
        try {
            const seconds = parseFloat(secondsString);
            if (response.usage.tokens) {
                const value =
                    Math.round((seconds / response.usage.tokens) * 100) / 100;

                return value;
            } else {
                return 0;
            }
        } catch (error) {
            return 0;
        }
    };

    const sortedResponses = responses.sort(
        (a, b) => b.time.toMillis() - a.time.toMillis()
    );

    return (
        <div className='flex w-full flex-col gap-8'>
            {loading && (
                <div className='mr-auto inline-block  rounded bg-white bg-opacity-5 p-4 shadow-border backdrop-blur-lg'>
                    <ThreeDots
                        height='12'
                        width='54'
                        radius='9'
                        color='#fff'
                        ariaLabel='three-dots-loading'
                        wrapperStyle={{ opacity: '.15' }}
                    />
                </div>
            )}
            {fullQuestion &&
                sortedResponses &&
                sortedResponses.length > 0 &&
                sortedResponses.map((response, i) => {
                    const currentResponse = response?.[
                        'llama'
                    ] as modelResponse;

                    return (
                        <ResponseCard
                            key={response.time.millisecond}
                            question={response?.question}
                            currentQuestion={i === 0}
                            formattedResponse={formattedResponse(
                                currentResponse
                            )}
                            responseTime={responseTime(currentResponse)}
                            pricing={currentResponse?.usage?.price}
                        />
                    );
                })}
        </div>
    );
};

export default ResponseList;
