import { InformationBundleCls, MessageCls, QuestionCls } from '../../utils/types';
import Question from '../question';
import InformationBundle from '../informationBundle';

type Props = {
    className?: string;
    message: MessageCls;
    messageNumber: number;
}

function Message(props: Props) {
    return (
        <>
        {props.message.type === 'question' ? (
            <Question question={(props.message.content as QuestionCls).question} className={props.className ? props.className : ''}/>
        ) : (
            <InformationBundle informationBundle={props.message.content as InformationBundleCls} className={props.className ? props.className : ''}></InformationBundle>
        )
        }
        </>
    )   
};

export default Message;