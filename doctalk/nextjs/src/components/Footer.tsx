'use client';

import { NavBar, NavMenu } from '@octoml/design-system';
import { ReactNode } from 'react';

const LinkItem = ({
    children,
    href
}: {
    children: ReactNode;
    href: string;
}) => (
    <li>
        <NavMenu.Link
            className='hover:bg-transparent'
            href={href}
            target='_blank'
        >
            {children}
        </NavMenu.Link>
    </li>
);

const Footer = () => (
    <footer>
        <NavBar className='w-screen border-none bg-transparent backdrop-filter-none'>
            <ul className='m-auto flex flex-col justify-center gap-2 text-center transition-spacing md:flex-row md:gap-0'>
                <LinkItem href='https://octo.ai/?utm_source=ask-llama'>
                    Powered by OctoAI
                </LinkItem>
                <LinkItem href='https://octo.ai/legals/privacy-policy/'>
                    Privacy Policy
                </LinkItem>
                <LinkItem href='https://octo.ai/legals/terms-of-use/'>
                    Terms of Use
                </LinkItem>
            </ul>
        </NavBar>
    </footer>
);

export default Footer;
