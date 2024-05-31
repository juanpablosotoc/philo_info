import { useState, PropsWithChildren, useRef } from 'react';
import styles from './index.module.css';
import eye_open from '../../SVG/icons/eye_open.svg';
import eye_closed from '../../SVG/icons/eye_closed.svg';

type Props = PropsWithChildren<{
    className?: string;
    label?: string;
}>

function PasswordInput(props: Props) {
    const [value, setValue] = useState('');
    const eye = useRef<HTMLImageElement>(null);
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
        let new_eye_src = eye_open;
        if (eye.current!.classList.contains("eye_open")) {
            eye.current!.classList.remove("eye_open")
            new_eye_src = eye_closed
        } else {
            eye.current!.classList.add("eye_open");
        };
        eye.current!.src = new_eye_src;

    };
    return (
        <div className={`${styles.card} ${props.className ? props.className : ''}`} ref={div}>
            <label htmlFor="short_text_input" className={styles.label}>{props.label ? props.label : 'Password'}</label>
            <img src={eye_closed} onClick={handleClick} className={styles.eye} alt="SVG Image" ref={eye}/>
            <input type="password" className={styles.input} name={'short_text_input'} value={value} onChange={handleChange} ref={passwordInput}/>
        </div>
    );
}

export default PasswordInput;
