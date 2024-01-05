import { Tag } from '@octoml/design-system';
import { FC } from 'react';
import SimpleBar from 'simplebar-react';

import 'simplebar-react/dist/simplebar.min.css';

interface ResponseCardProps {
    question: string;
    formattedResponse: JSX.Element | string;
    responseTime: number;
    currentQuestion?: boolean;
    pricing?: number;
}

const ResponseCard: FC<ResponseCardProps> = ({
    question,
    formattedResponse,
    responseTime,
    currentQuestion,
    pricing
}) => {
    const tagClasses = 'bg-white bg-opacity-5 shadow-border';

    return (
        <div className='flex w-full flex-col justify-between gap-6'>
            <div className='flex flex-col gap-6'>
                <div className='relative mr-auto flex w-full flex-col gap-4 rounded bg-white bg-opacity-5 p-4 shadow-border backdrop-blur-lg'>
                    {!currentQuestion && (
                        <p>
                            <i>Q: {question}</i>
                        </p>
                    )}
                    <SimpleBar
                        style={{ height: 250, width: '100%' }}
                        autoHide={false}
                    >
                        <div
                            className={`pr-12 ${
                                currentQuestion ? '' : 'pt-1'
                            } text-xl font-normal leading-8`}
                        >
                            {formattedResponse}
                        </div>
                    </SimpleBar>
                </div>
            </div>
            <div className='flex items-start gap-5'>
                <Tag className={tagClasses}>
                    {responseTime
                        ? `${responseTime} secs/token`
                        : 'Not available'}
                </Tag>
                <Tag className={tagClasses}>
                    {pricing ? `${pricing} cents` : 'Not available'}
                </Tag>
            </div>
        </div>
    );
};

export default ResponseCard;
