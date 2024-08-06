import styles from './styles.module.css';


export default function Sequence(props: React.PropsWithChildren<{}>) {
    return (
    <div className={styles.sequence}>
        {props.children}
    </div>
    )
}