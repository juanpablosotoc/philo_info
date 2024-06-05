import styles from './index.module.css';
import Message from '../message';
import { MessageCls } from '../../utils/types';

type Props = {
    messages: MessageCls[];
    className?: string;
    setCurrentMessage: React.Dispatch<React.SetStateAction<number>>;
}

function Messages (props: Props) {
    return (
        <>
            {props.messages.map((message, index) =>{
            return (
                <>
                <Message message={message} setCurrentMessage={props.setCurrentMessage} key={index + 'message'} messageNumber={index} className={styles.message}></Message>
                {index < (props.messages.length -1) ? <br className={styles.br} key={index + 'br'}/> : ''}
                </>
            )
            })}
        </>
    )
};

export default Messages;
