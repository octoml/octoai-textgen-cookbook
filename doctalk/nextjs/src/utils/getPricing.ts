export interface Pricing {
    prompt_tokens: number;
    input_price: number;
    output_tokens: number;
    output_price: number;
}

/**
 * Calculates pricing based on the provided numbers.
 * @param prompt_tokens - Number of prompt tokens used.
 * @param input_price - Price per input token.
 * @param output_tokens - Number of output tokens used.
 * @param output_price - Price per output token.
 * @returns Calculated pricing as cents.
 */

export const getPricing = ({
    prompt_tokens,
    input_price,
    output_tokens,
    output_price
}: Pricing): number => {
    const inputPrice = prompt_tokens * input_price;

    const outputPrice = output_tokens * output_price;

    const totalPrice = (inputPrice + outputPrice) / 1000;

    return Math.round(totalPrice * 10000) / 10000;
};
