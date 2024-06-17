import { InformationBundleCls, MessageCls } from '../../utils/types';
import styles from './index.module.css';
import Links from '../links';
import Texts from '../texts';
import Files from '../files';
import MediumCard from '../medium_card';

type Props = {
    className?: string;
    message: MessageCls;
    messageNumber: number;
}

function Message(props: Props) {
    return (
        <MediumCard className={`${props.className ? props.className : ''} ${styles.wrapper}`}>
            <div className={styles.input}>
                    {/* The add icon */}
                    <div className={styles.iconWrapper}>
                        <svg width="24" className={styles.icon} height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 5V19" stroke="#F7F7F7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M5 12H19" stroke="#F7F7F7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                    </div>
                    <div className={styles.informationBundle}>
                        {props.message.content.texts.length ? <Texts texts={props.message.content.texts}></Texts> : ''}
                        {props.message.content.links.length ? <Links links={props.message.content.links}></Links> : ''}
                        {props.message.content.files.length ? <Files files={props.message.content.files}></Files> : ''}
                    </div>
                </div>
            <div className={styles.output}>

            </div>
        </MediumCard>
        )
};

export default Message;

