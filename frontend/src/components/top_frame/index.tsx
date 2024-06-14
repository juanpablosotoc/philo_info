import styles from './index.module.css';
import { Link } from 'react-router-dom';


type Props = {
    active: 'home' | 'store';
}

function TopFrame(props: Props) {
    return (
        <div className={styles.wrapper}>
            <div className={styles.left + ' ' + styles.innerWrapper + ' ' + (props.active === 'home' ? styles.active : '')}>
                <div className={styles.modal}></div>
                <Link to='/' className={styles.link}>Home</Link>
            </div>
            <div className={styles.right + ' ' + styles.innerWrapper + ' ' + (props.active === 'store' ? styles.active : '')}>
                <div className={styles.modal}></div>
                <Link to='/store' className={styles.link}>Store</Link>
            </div>
        </div>
    )
};

export default TopFrame;
