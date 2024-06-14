import styles from './index.module.css';
import Lines from '../lines';

function Footer () {
    return (
        <footer className={styles.footer}>
            <p className={styles.infoWrapper}>
                <a className={styles.a}>API</a>|
                <a className={styles.a}>Privacy</a>| 
                <a className={styles.a}>Terms</a>
            </p>
            <Lines></Lines>
        </footer>
    )
};

export default Footer;
