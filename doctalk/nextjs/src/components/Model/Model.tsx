import CompanyCard from './ModelCard';

import MetaLogo from '@/assets/svg/MetaLogo.svg';

const Model = () => (
    <div className='flex w-full flex-col gap-12'>
        <CompanyCard
            icon={{ src: MetaLogo, alt: 'Meta Logo' }}
            name='Code Llama'
            openSource={true}
            description='A 34B parameter open source model from Meta AI.'
        />
    </div>
);

export default Model;
