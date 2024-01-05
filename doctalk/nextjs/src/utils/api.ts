import axios from 'axios';

export const getAnswers = async (question: string, dataSource: string) => {
    try {
        const response = await axios.post(
            `${process.env.API_URL}/askllama`,
            {
                prompt: question,
                data_source: dataSource
            },
            {
                headers: {
                    'Content-type': 'application/json',
                    'x-api-key': `${process.env.API_KEY}`
                }
            }
        );

        return response.data;
    } catch (error) {
        console.error(error);

        return {
            error
        };
    }
};
