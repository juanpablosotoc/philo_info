import styles from './styles.module.css';


interface Props {
    author: string;
}

export default function Quote(props: React.PropsWithChildren<Props>) {
    return (
        <div className={styles.wrapper}>
            <p>"{props.children}"</p>
            <p className={styles.author}><i>{props.author}</i></p>
        </div>
    )
}