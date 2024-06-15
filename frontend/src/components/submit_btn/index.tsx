import { PropsWithChildren } from 'react';
import styles from './index.module.css';

type Props = PropsWithChildren<{
    className?: string;
    label?: string;
    onClick?: () => void;
    theme: 'light' | 'dark';
}>


function SubmitBtn(props: Props) {
    return (
        <input type="submit" value={props.label ? props.label : 'Submit'} className={`${styles.submit_btn} ${props.className ? props.className : ''} ${props.theme === 'dark' ? styles.dark : styles.light}`} onClick={props.onClick ? props.onClick : ()=>{}}/>
    );
}

export default SubmitBtn;
