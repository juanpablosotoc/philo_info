import { useState, PropsWithChildren, useRef } from 'react';
import styles from './index.module.css';

type Props = PropsWithChildren<{
    className?: string;
    label?: string;
    type: 'email' | 'text';
    color: "white" | "black";
    name: string;
    handleFocusOut?: () => void;
    setTopicHasChanged?: React.Dispatch<React.SetStateAction<boolean>>;
    value: string;
    setValue: React.Dispatch<React.SetStateAction<string>>;
}>

function ShortTextInput(props: Props) {
    let initialValue = props.value ? props.value : '';
    const div = useRef<HTMLDivElement>(null);
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.value.length) div.current!.classList.add(styles.active)
        else div.current!.classList.remove(styles.active);
        props.setValue(event.target.value);
        if (props.setTopicHasChanged) props.setTopicHasChanged(true);
    };
    const colorClasses = {'white': styles.white, 'black': styles.black};
    return (
        <div className={`${styles.card} ${colorClasses[props.color]} ${props.className ? props.className : ''} ${initialValue ? styles.active: ''}`} ref={div}>
            <label htmlFor={props.name} className={styles.label}>{props.label ? props.label : 'Email address'}</label>
            <input type={props.type} className={styles.input} name={props.name} value={props.value} onChange={handleChange} onBlur={props.handleFocusOut ? props.handleFocusOut : ()=>{}} />
        </div>
    );
}

export default ShortTextInput;
