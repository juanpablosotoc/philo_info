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
    const processedInfosTexts: any = {};
    if (props.message.processedInfos) {
        for (let processed_info of props.message.processedInfos) {
            if (!processed_info.info) continue;
            if (processed_info.id in processedInfosTexts) {
                processedInfosTexts[processed_info.id] = processedInfosTexts[processed_info.id].concat(processed_info.info);
            } else {
                processedInfosTexts[processed_info.id] = processed_info.info;
            }
        }
    };
    return (
        <MediumCard innerClassName={`${props.className ? props.className : ''} ${styles.wrapper}`}>
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
            {processedInfosTexts && (
                <div className={styles.processedInfoWrapper}>
                    <div className={styles.labelWrapperWrapper}>
                        <p className={styles.labelWrapper}>
                            <span className={styles.label + ' ' + styles.first}>Processed Information</span>
                            <span className={styles.label + ' ' + styles.last}>Processed Information</span>
                        </p>  
                        <hr className={styles.underline}/>
                    </div>
                    <div className={styles.processed_infos}>
                            {
                            Object.keys(processedInfosTexts).map((key, index) => {
                            return (
                                <p className={styles.processed_info} key={'processed-info-' + index}>{processedInfosTexts[key]}</p>
                            )
                            })
                        }
                    </div>
                </div>
            )}
            <div className={styles.possible_outputs}>
                {props.message.possible_outputs?.map((output, index) => {
                    return (
                        <p className={styles.output_choice} key={'output-choice-' + index}>{output}</p>
                    )
                })}
            </div>
        </MediumCard>
        )
};

export default Message;

