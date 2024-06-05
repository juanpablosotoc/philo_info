import { InformationBundleCls, MessageCls, QuestionCls } from '../../utils/types';
import styles from './index.module.css';
import Question from '../question';
import InformationBundle from '../informationBundle';
import { useEffect, useRef } from 'react';

type Props = {
    className?: string;
    message: MessageCls;
    messageNumber: number;
    setCurrentMessage: React.Dispatch<React.SetStateAction<number>>;
}

function Message(props: Props) {
    const element = useRef<HTMLElement>(null);

    useEffect(() => {
        const observer = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) props.setCurrentMessage(props.messageNumber + 1);
        });
        console.log(element.current); // null
          observer.observe( element.current!);
        }
    , []);
    
    return (
        <>
        {props.message.type === 'question' ? (
            <Question question={(props.message.content as QuestionCls).question} questionNumber={props.messageNumber} setQuestionNumber={props.setCurrentMessage} className={props.className ? props.className : ''} myRef={element}/>
        ) : (
            <InformationBundle informationBundle={props.message.content as InformationBundleCls} className={props.className ? props.className : ''} myRef={element}></InformationBundle>
        )
        }
        </>
    )   
};

export default Message;