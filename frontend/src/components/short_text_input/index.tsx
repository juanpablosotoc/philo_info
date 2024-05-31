import { useState, PropsWithChildren, useRef } from 'react';
import styles from './index.module.css';

type Props = PropsWithChildren<{
    className?: string;
    label?: string;
}>

function ShortTextInput(props: Props) {
    const [value, setValue] = useState('');
    const div = useRef<HTMLDivElement>(null)
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.value.length) {
            div.current!.className += ` ${styles.active}`;
        } else {
            div.current!.className = styles.card + ` ${props.className ? props.className : ''}`;
        };
        setValue(event.target.value);
    };

    return (
        <div className={`${styles.card} ${props.className ? props.className : ''}`} ref={div}>
            <label htmlFor="short_text_input" className={styles.label}>{props.label ? props.label : 'Email address'}</label>
            <input type="text" className={styles.input} name={'short_text_input'} value={value} onChange={handleChange} />
        </div>
    );
}

export default ShortTextInput;
