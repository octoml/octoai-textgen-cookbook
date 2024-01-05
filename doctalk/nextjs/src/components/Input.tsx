'use client';

import { Alert, Icon, InputGroup } from '@octoml/design-system';
import axios from 'axios';
import { DateTime } from 'luxon';
import { ChangeEvent, KeyboardEventHandler, useEffect } from 'react';

import Dropdown from './Header/Dropdown';

import useStore from '@/store/useStore';
import { getPricing } from '@/utils/getPricing';

const Input = () => {
    const {
        dataSource,
        setLoading,
        question,
        setQuestion,
        fullQuestion,
        setFullQuestion,
        responses,
        setResponses,
        userChangedData,
        loading,
        error,
        setError
    } = useStore();
    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    const generateResponse = async () => {
        setLoading(true);
        setFullQuestion(question);
        scrollToTop();
        try {
            const llamaResponse = await axios.post('/api/askModel', {
                question,
                dataSource
            });
            let usage_llama = null;

            try {
                usage_llama = JSON.parse(
                    llamaResponse.data.usage_llm2.replace(/'/g, '"')
                );
            } catch (errorParseLlm) {
                console.error('Llama error', errorParseLlm);
            }

            setResponses([
                {
                    time: DateTime.now(),
                    llama: {
                        response: llamaResponse.data.message_llm2.replace(
                            /^\n+|\n+$/g,
                            ''
                        ),
                        usage: {
                            price: usage_llama
                                ? getPricing({
                                      prompt_tokens: usage_llama.prompt_tokens,
                                      input_price: 0.06,
                                      output_tokens:
                                          usage_llama.completion_tokens,
                                      output_price: 0.19
                                  })
                                : 0,
                            tokens: usage_llama
                                ? usage_llama.completion_tokens
                                : 0
                        }
                    },
                    question,
                    questionId: ''
                },
                ...responses
            ]);
            setLoading(false);
            setError(false);
        } catch (err) {
            setLoading(false);
            setError(true);
            console.error(err);

            return;
        }
    };

    const changeQuestion = (event: ChangeEvent<HTMLInputElement>) => {
        setQuestion(event.target.value);
    };

    useEffect(() => {
        if (fullQuestion && userChangedData) {
            generateResponse();
        }
    }, [fullQuestion]);

    const onKeyPress: KeyboardEventHandler<HTMLDivElement> = async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            await generateResponse();
        }
    };

    const handleClick = () => {
        generateResponse();
    };

    return (
        <>
            {!fullQuestion && <Dropdown large />}

            <InputGroup className='w-full flex-wrap gap-6 overflow-visible border-transparent p-0 focus-within:border-0 md:flex-nowrap md:gap-0 md:overflow-hidden md:border-gray-500 md:focus-within:border'>
                <InputGroup.Textbox
                    className={`w-full border border-gray-500 transition-spacing md:border-0 md:border-transparent 
                    ${
                        fullQuestion
                            ? 'p-3 text-xl'
                            : 'p-3 text-lg md:p-6 md:text-2xl'
                    }  `}
                    placeholder='Go for it, ask a question'
                    onChange={changeQuestion}
                    onKeyDown={onKeyPress}
                    value={question}
                />
                <InputGroup.Button
                    variant='secondary'
                    className='group w-full justify-center rounded border !border-gray-800 text-lg hover:bg-gradient-teal md:-m-6 md:h-auto md:w-auto md:flex-shrink-0 md:flex-grow md:self-stretch md:rounded-none md:border-none md:px-10'
                    onClick={handleClick}
                    disabled={loading}
                >
                    <span className='group-hover:text-gray-900'>
                        See Responses
                    </span>
                    <Icon icon='Send03' className='group-hover:text-gray-900' />
                </InputGroup.Button>
            </InputGroup>
            {error && !loading && (
                <div className='fixed bottom-0 left-0 z-50 w-full px-8 py-4 transition-spacing lg:px-80px xl:px-160px'>
                    <Alert className='!bg-error-500 !bg-opacity-90'>
                        <Alert.Icon icon='XCircle' />
                        <Alert.Content>
                            <Alert.Title>
                                There was an error retrieving the response,
                                please try again.
                            </Alert.Title>
                        </Alert.Content>
                        <Alert.Close className='hover:!text-error-100' />
                    </Alert>
                </div>
            )}
        </>
    );
};

export default Input;
