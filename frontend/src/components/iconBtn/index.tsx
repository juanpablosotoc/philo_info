import styles from './index.module.css';

type Props = {
    iconSrc: string;
    altText: string;
    className?: string;
}

function IconBtn(props: Props) {
    return (
        <img src={props.iconSrc} alt={props.altText} className={`${styles.icon} ${props.className ? props.className : ''}`}/>
    );
};

export default IconBtn;
