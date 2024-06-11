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
            <div className={styles.innerWrapper}>
                <img src={brandLogo} alt={`${props.type} logo`} className={styles.brandLogo} />
                <p className={styles.label}>Continue with <span className={styles.capitalize}>{props.type}</span></p>
            </div>
            <div className={styles.innerWrapper + ' ' + styles.lastInnerWrapper}>
                <img src={brandLogo} alt={`${props.type} logo`} className={styles.brandLogo} />
                <p className={styles.label}>Continue with <span className={styles.capitalize}>{props.type}</span></p>
            </div>
        </div>
    );
}

export default OAuth;
