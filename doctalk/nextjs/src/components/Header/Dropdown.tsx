'use client';

import { Button, Label, Select } from '@octoml/design-system';
import { FC, useState } from 'react';

import useStore from '@/store/useStore';

export const docSources = [
    {
        value: 'octoai_docs',
        name: 'OctoAI Docs'
    },
    {
        value: 'pinecone',
        name: 'Pinecone Docs'
    }
];

interface DropdownProps {
    large?: boolean;
    isScrolled?: boolean;
}
const Dropdown: FC<DropdownProps> = ({ large = false, isScrolled = false }) => {
    const [selected, setSelected] = useState('octoai_docs');

    const { setDataSource, dataSource, loading } = useStore();

    const handleSelect = (val: string) => {
        setSelected(val);
        setDataSource(val);
    };

    const currentSelection =
        docSources.find((source) => source.value === dataSource)?.name ||
        'Select Source';

    return (
        <Label
            className={`${large ? 'w-full text-center' : 'place-self-end self-center'
                } ${isScrolled ? 'ml-3' : 'w-full md:w-auto'
                }   flex-row flex-wrap items-center justify-center gap-3  md:flex-nowrap`}
        >
            <span
                className={`${large ? 'text-xl' : ''} 
                ${isScrolled ? 'hidden md:block' : ''}  
                font-light`}
            >
                Data Source
            </span>
            <Select
                value={selected}
                onChange={(val) => handleSelect(val)}
                disabled={loading}
            >
                <Select.Trigger asChild>
                    <Button
                        appearance='listbox'
                        variant='secondary'
                        className={`${large ? 'py-6 text-2xl' : ''} 
                        ${isScrolled ? 'px-3 text-xs' : ''} 
                        `}
                    >
                        {currentSelection}
                        <Button.Icon icon='ChevronDown' />
                    </Button>
                </Select.Trigger>
                <Select.Content>
                    {docSources.map((source) => (
                        <Select.Item
                            key={source.value}
                            value={source.value}
                            className='text-left '
                        >
                            {source.name}
                        </Select.Item>
                    ))}
                </Select.Content>
            </Select>
        </Label>
    );
};

export default Dropdown;
