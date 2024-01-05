'use client';

import { Heading1, NavBar, NavMenu } from '@octoml/design-system';
import Image from 'next/image';
import { useEffect, useState } from 'react';

import Dropdown from './Dropdown';

import LogomarkWhite from '@/assets/svg/LogomarkWhite.svg';

const TopNav = () => {
    const [isScrolled, setIsScrolled] = useState(false);

    useEffect(() => {
        const toggleScrolled = () => {
            if (window.scrollY > 1) {
                setIsScrolled(true);
            } else {
                setIsScrolled(false);
            }
        };
        window.addEventListener('scroll', toggleScrolled, { passive: true });

        return () => {
            window.removeEventListener('scroll', toggleScrolled);
        };
    }, [isScrolled]);

    return (
        <header
            className={`sticky top-0 z-50 transition-colors  ${isScrolled ? 'bg-gray-900 bg-opacity-95' : 'bg-transparent'
                }`}
        >
            <NavBar
                className={`py-3 transition-spacing ${isScrolled ? 'md:py-3' : 'md:py-6'
                    }`}
            >
                <div
                    className={`flex w-full flex-wrap justify-center  transition-spacing lg:grid lg:grid-cols-3 ${isScrolled ? 'gap-y-1' : 'gap-y-3'
                        }`}
                >
                    <NavMenu.Link
                        href='https://octoml.ai/?utm_source=ask-llama'
                        target='_blank'
                        className={` self-start transition-size hover:bg-transparent ${isScrolled ? 'w-9' : 'w-12'
                            }`}
                    >
                        <Image src={LogomarkWhite} alt='OctoAI Logo' />
                    </NavMenu.Link>

                    <NavMenu.Link
                        href='/'
                        className='flex flex-nowrap gap-1 self-center hover:bg-transparent md:m-auto'
                    >
                        <Heading1 className='text-xl text-white md:text-3xl'>
                            DocTalk
                        </Heading1>
                    </NavMenu.Link>

                    <Dropdown isScrolled={isScrolled} />
                </div>
            </NavBar>
        </header>
    );
};

export default TopNav;
