import styles from './styles.module.css';
import HorConnectorLine from '../../icons/horConnectorLine';
import Arrow from '../../icons/arrow';


export default function SequenceEvent(props: React.PropsWithChildren<{title: string}>) {
    return (
        <div className={styles.sequenceEvent}>
            <p className={styles.title}><b>{props.title}</b></p>
            {props.children}
            <Arrow className={styles.arrow}></Arrow>
        </div>
    );
}