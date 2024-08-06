import styles from './index.module.css';
import { MessageCls, DefaultQuestionsCls, InfoMessageCls, RequestMessageCls } from '../../utils/types';
import WelcomMessage from '../welcomeMessage';
import { useEffect, useRef } from 'react';
import InfoBundle from '../infoBundle';
import ProcessedInfos from '../processedInfos';
import Logo from '../icons/logo';
import Profile from '../icons/profile';
import Copy from '../icons/copy';
import Speaker from '../icons/speaker';
import Pen from '../icons/pen';

type Props = {
    messages: MessageCls[];
    className?: string;
    questions: DefaultQuestionsCls[];
}

function Messages (props: Props) {
    const wrapper = useRef<HTMLDivElement>(null);
    useEffect(()=>{
        // scroll to bottom on wrapper
        wrapper.current!.scrollTop = wrapper.current!.scrollHeight;
    }, [props.messages])
    return (
        <div className={props.className + ' ' + styles.wrapper} ref={wrapper}>
        {props.messages.length ? (
                props.messages.map((message, index) => {
                return (
                    <>
                    {message.request_type === 'info' ? (
                        <>
                            <InfoBundle infoBundle={(message.content as InfoMessageCls)} className={styles.input}></InfoBundle>
                            <div className={styles.output}>
                                <Logo></Logo>
                                <ProcessedInfos processedInfos={(message.content as InfoMessageCls).processedInfos}></ProcessedInfos>
                                <p className={styles.messageContent}>{(message.content as InfoMessageCls).possible_outputs}</p>
                                <div className={styles.iconsWrapper}>
                                    <Speaker></Speaker>
                                    <Copy></Copy>
                                    <Pen></Pen>
                                </div>
                            </div>
                        </>
                    ) : (
                        <>
                            <div className={styles.input}>
                                <Profile></Profile>
                                <p className={styles.messageContent}>{(message.content as RequestMessageCls).content}</p>
                            </div>
                            <div className={styles.output}>
                                <Logo></Logo>
                                <p className={styles.messageContent}>{(message.content as RequestMessageCls).response}</p>
                                <div className={styles.iconsWrapper}>
                                    <Speaker></Speaker>
                                    <Copy></Copy>
                                    <Pen></Pen>
                                </div>
                            </div>
                        </>
                    )}
                    </>
                )})) : (
                <WelcomMessage className={styles.message} questions={props.questions}></WelcomMessage>         
            )}
        </div>
    )
};

export default Messages;
