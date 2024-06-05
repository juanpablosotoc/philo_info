import styles from './index.module.css';
import x_white from '../../SVG/icons/x_white.svg';
import x_grey from '../../SVG/icons/x_grey.svg';

type Props = {
    className?: string;
    label: string;
    handleXClick?: any;
};

function SmallCard (props: Props) {
    return (
        <div className={`${props.className} ${styles.cardWrapper}`}>
            <p>{props.label}</p>
            {props.handleXClick && (
            <div className={styles.iconsWrapper} onClick={props.handleXClick}>
                <img src={x_grey} alt="grey x" className={styles.grey}/>
                <img src={x_white} alt="white x" className={styles.white} />
            </div>
            )}
        </div>
    )
};

export default SmallCard;
