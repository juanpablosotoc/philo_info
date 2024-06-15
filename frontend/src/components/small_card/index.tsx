import styles from './index.module.css';

type Props = {
    className?: string;
    label: string;
    handleXClick?: any;
};

function SmallCard (props: Props) {
    const wrapper_class = `${props.className} ${styles.cardWrapper} ${props.handleXClick ? styles.clickable : ''}`;
    return (
        <div className={wrapper_class}>
            <p>{props.label}</p>
            {props.handleXClick && (
                // The x icon
            <svg width="24" height="24" className={styles.x} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="#F7F7F7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M6 6L18 18" stroke="#F7F7F7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            )}
        </div>
    )
};

export default SmallCard;
