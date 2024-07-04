import { useState, PropsWithChildren, useRef } from 'react';
import styles from './index.module.css';
import eye_open from '../../SVG/icons/eye_open.svg';
import eye_closed from '../../SVG/icons/eye_closed.svg';
import Eye from '../icons/eye';

type Props = PropsWithChildren<{
    className?: string;
    label?: string;
    name: string;
    hidden?: boolean;
}>

function PasswordInput(props: Props) {
    const [value, setValue] = useState('');
    const [isInvisible, setIsInvisible] = useState(true);
    const div = useRef<HTMLDivElement>(null);
    const passwordInput = useRef<HTMLInputElement>(null);
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.value.length) {
            div.current!.className += ` ${styles.active}`;
        } else {
            div.current!.className = styles.card + ` ${props.className ? props.className : ''}`;
        };
        setValue(event.target.value);
    };
    const handleClick = () => {
        /* Show/hide text */
        let opposite_input_type = "text";
        if (passwordInput.current!.type === "text") opposite_input_type = "password";
        passwordInput.current!.type = opposite_input_type;
        /* change eye */
        setIsInvisible((prev) => !prev);
    };
    return (
        <div className={`${styles.card} ${props.hidden ? styles.hidden : ''} ${props.className ? props.className : ''}`} ref={div}>
            <label htmlFor={props.name} className={styles.label}>{props.label ? props.label : 'Password'}</label>
            <Eye onClick={handleClick} className={styles.eye} invisible={isInvisible}></Eye>
            <input type="password" className={styles.input} name={props.name} value={value} onChange={handleChange} ref={passwordInput}/>
        </div>
    );
}

export default PasswordInput;
