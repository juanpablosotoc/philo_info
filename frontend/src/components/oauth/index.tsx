import { PropsWithChildren } from 'react';
import styles from './index.module.css';
import google from '../../SVG/brands/google.svg';
import apple from '../../SVG/brands/apple.svg';
import microsoft from '../../SVG/brands/microsoft.svg';

type Props = PropsWithChildren<{
    className?: string;
    type: "apple" | "microsoft" | "google";
}>


function OAuth(props: Props) {
    let brandLogo = microsoft;
    if (props.type === "apple") {
        brandLogo = apple;
    }
    else if (props.type === "google") {
        brandLogo = google
    }
    return (
        <div className={styles.card}>
            <img src={brandLogo} alt={`${props.type} logo`} className={styles.brandIcon} />
            <div className={styles.wrapper}>
                <p className={styles.label}>Continue with <span className={styles.capitalize}>{props.type}</span></p>
                <hr className={styles.underline}/>
            </div>
            {/* The chevron icon */}
            {/* <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.chevronIcon}>
                <path d="M13.2157 25L25 13L13.2157 1" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M1 13L25 13" stroke="black" stroke-width="2" stroke-linecap="round" className={styles.chevronLine}/>
            </svg> */}

            <svg xmlns="http://www.w3.org/2000/svg" className={styles.chevronIcon} width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path fill="currentColor" className={styles.chevron} d="M7.28033 3.21967C6.98744 2.92678 6.51256 2.92678 6.21967 3.21967C5.92678 3.51256 5.92678 3.98744 6.21967 4.28033L7.28033 3.21967ZM11 8L11.5303 8.53033C11.8232 8.23744 11.8232 7.76256 11.5303 7.46967L11 8ZM6.21967 11.7197C5.92678 12.0126 5.92678 12.4874 6.21967 12.7803C6.51256 13.0732 6.98744 13.0732 7.28033 12.7803L6.21967 11.7197ZM6.21967 4.28033L10.4697 8.53033L11.5303 7.46967L7.28033 3.21967L6.21967 4.28033ZM10.4697 7.46967L6.21967 11.7197L7.28033 12.7803L11.5303 8.53033L10.4697 7.46967Z"></path>
                <path className={styles.chevronIconStem} stroke="currentColor" d="M1.75 8H11" stroke-width="1.5" stroke-linecap="round"></path>
            </svg>
        </div>
    );
}

export default OAuth;
