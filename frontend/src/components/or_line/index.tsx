import { PropsWithChildren } from 'react';
import styles from './index.module.css';

type Props = PropsWithChildren<{
    className?: string;
}>


function OrLine(props: Props) {
    return (
        <div className={styles.div}>
            <hr className={styles.hr}/>
            <p className={styles.label}>or</p>
            <hr className={styles.hr}/>
        </div>
    );
}

export default OrLine;
