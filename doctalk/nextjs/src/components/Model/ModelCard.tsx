'use client';

import Image, { StaticImageData } from 'next/image';
import { FC } from 'react';

import OpenSource from './OpenSource';

import useStore from '@/store/useStore';

interface CompanyCardProps {
    icon: {
        src: string | StaticImageData;
        alt: string;
    };
    name: string;
    description: string;
    openSource?: boolean;
}

const ModelCard: FC<CompanyCardProps> = ({
    icon,
    name,
    description,
    openSource
}) => {
    const { fullQuestion } = useStore();

    const headingClasses = `${fullQuestion
            ? 'text-2xl'
            : 'text-3xl desktop-lg:text-5xl  desktop-xl:text-hd-lg'
        } font-medium transition-font`;

    const descClasses = `text-center font-normal  ${fullQuestion
            ? 'leading-6'
            : 'text-xl leading-8 desktop-lg:text-dsc-lg desktop-lg:leading-10 transition-font'
        }`;

    return (
        <div className='flex w-full flex-col flex-wrap justify-center gap-6'>
            <div className='flex flex-col items-center justify-center gap-6 xl:flex-row'>
                <Image src={icon.src} alt={icon.alt} />
                <h2 className={headingClasses}>{name}</h2>
                {openSource && <OpenSource />}
            </div>
            <p className={descClasses}>{description}</p>
        </div>
    );
};

export default ModelCard;
