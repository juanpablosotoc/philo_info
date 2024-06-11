import styles from './index.module.css';
import Lines from '../lines';

function Footer () {
    return (
        <footer className={styles.footer}>
            <p className={styles.infoWrapper}>
                <span>API</span> |
                <span> Privacy</span> |
                <span>Terms</span>
            </p>
            <Lines></Lines>
        </footer>
    )
};

export default Footer;
