import styles from './styles.module.css';


export default function SequenceEvent(props: React.PropsWithChildren<{title: string}>) {
    return (
        <div className={styles.sequenceEvent}>
            <div className={styles.metadata}>
                <p className={styles.title}>{props.title}</p>
            </div>
            <div className={styles.content}>{props.children}</div>
        </div>
    );
}