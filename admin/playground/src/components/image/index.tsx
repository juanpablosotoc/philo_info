import styles from './styles.module.css';


export default function Image(props: React.PropsWithChildren<{}>) {
    return (
        <div className={styles.image}>
            {props.children}
        </div>
    );
}