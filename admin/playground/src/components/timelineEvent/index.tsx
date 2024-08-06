import styles from './styles.module.css';
import ConnectorLine from '../../icons/connectorLine';

interface Props {
    date: string;
    color: 'primary' | 'secondary';
}

export default function TimelineEvent(props: React.PropsWithChildren<Props>) {
    return (
        <div className={styles.timelineEvent}>
            <hr className={props.color === 'secondary' ? styles.secondary : ''} />
            <ConnectorLine color={props.color} />
            <div className={styles.content}>
            <p className={styles.date}><i>{props.date}</i></p>
            {props.children}
            </div>
        </div>
    );
};