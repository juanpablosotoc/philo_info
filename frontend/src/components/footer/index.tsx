import styles from './index.module.css';
import Lines from '../lines';
import MyLink from '../my_link';

function Footer () {
    return (
        <footer className={styles.footer}>
            <p className={styles.infoWrapper}>
                <MyLink to='/api' className={styles.a}>API</MyLink>|
                <MyLink to='/privacy' className={styles.a}>Privacy</MyLink>|
                <MyLink to='/terms' className={styles.a}>Terms</MyLink>
            </p>
            <Lines></Lines>
        </footer>
    )
};

export default Footer;
