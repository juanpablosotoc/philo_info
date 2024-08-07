import styles from './styles.module.css';

export default function Frame(props: React.PropsWithChildren<{}>) {
    return (
        <div className={styles.frame}>
            {props.children}
        </div>
    );
}