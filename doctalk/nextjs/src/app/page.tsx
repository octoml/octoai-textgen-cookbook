import EntryPoint from '@/components/EntryPoint';

export default function Home() {
    return (
        <main className='m-auto w-full max-w-container px-8 pb-8 pt-12 md:pt-20 lg:px-80px xl:px-160px xl:pt-16'>
            <EntryPoint />
            <p className='mt-20 text-center italic'>
                Please evaluate model response quality independently before
                using these for production use cases
            </p>
        </main>
    );
}
