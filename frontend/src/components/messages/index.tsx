import styles from './index.module.css';
import Message from '../message';
import { MessageCls, QuestionCls } from '../../utils/types';
import WelcomMessage from '../welcomeMessage';

type Props = {
    messages: MessageCls[];
    className?: string;
    questions: QuestionCls[];
}

function Messages (props: Props) {
    return (
        <div className={props.className + ' ' + styles.wrapper}>
            {props.messages.length ? (props.messages.map((message, index) =>{
            return (
                <>
                <br className={styles.br} key={index + 'br'}/>
                <Message message={message} key={index + 'message'} messageNumber={index} className={styles.message}></Message>
                </>
            )
            })) : (
                <>
                <br className={styles.br}/>
                <WelcomMessage className={styles.message} questions={props.questions}></WelcomMessage>
                <br className={styles.br}/>
                <br className={styles.br}/>
                <WelcomMessage className={styles.message} questions={props.questions}></WelcomMessage>
                <br className={styles.br}/>
                <br className={styles.br}/>
                <WelcomMessage className={styles.message} questions={props.questions}></WelcomMessage>
                <br className={styles.br}/>
                <br className={styles.br}/>
                <WelcomMessage className={styles.message} questions={props.questions}></WelcomMessage>                
                </>
            )}
        </div>
    )
};

export default Messages;
