import { Link } from 'react-router-dom';
import styles from './index.module.css';
import { PropsWithChildren } from 'react'

type Props = {
    className?: string;
    to: string;
}

function MyLink(props: PropsWithChildren<Props>) {
    return (
        <Link to={props.to} className={styles.wrapper  + ' ' + (props.className ? props.className : '')}>
            <span className={styles.link + ' ' + styles.first}>{props.children}</span>
            <span className={styles.link + ' ' + styles.last}>{props.children}</span>
        </Link>
    )
};


export default MyLink;
