import styles from './index.module.css';

type Props = {
    className?: string;
    topBottom: 'top' | 'bottom';
}

function Modal (props: Props) {
    return (
        <div className={`${styles.modal} ${props.topBottom === 'bottom' ? styles.bottom : styles.top} ${props.className ? props.className : ''}`}></div>
    )
};

export default Modal;