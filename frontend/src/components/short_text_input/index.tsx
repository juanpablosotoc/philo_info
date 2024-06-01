import { useState, PropsWithChildren, useRef } from 'react';
import styles from './index.module.css';

type Props = PropsWithChildren<{
    className?: string;
    label?: string;
    name: string;
}>

function ShortTextInput(props: Props) {
    const [value, setValue] = useState('');
    const div = useRef<HTMLDivElement>(null);
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.value.length) div.current!.classList.add(styles.active)
        else div.current!.classList.remove(styles.active);
        setValue(event.target.value);
    };
    return (
        <div className={`${styles.card} ${props.className ? props.className : ''}`} ref={div}>
            <label htmlFor={props.name} className={styles.label}>{props.label ? props.label : 'Email address'}</label>
            <input type="text" className={styles.input} name={props.name} value={value} onChange={handleChange} />
        </div>
    );
}

export default ShortTextInput;
