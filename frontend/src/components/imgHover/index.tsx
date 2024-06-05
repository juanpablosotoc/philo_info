import styles from './index.module.css';

type Props = {
    className?: string;
    img: string;
    imgHover: string;
    altText: string;
    hoverClassName?: string;
    imgClassName?: string;
}

function ImgHover (props: Props) {
    return (
        <div className={`${props.className ? props.className : ''} ${styles.wrapper}`}>
            <img src={props.img} alt={props.altText} className={`${styles.img} ${props.imgClassName ? props.imgClassName : ''}`}/>
            <img src={props.imgHover} alt={props.altText} className={`${styles.imgHover} ${props.hoverClassName ? props.hoverClassName : ''}`} />
        </div>
    )
};

export default ImgHover;
