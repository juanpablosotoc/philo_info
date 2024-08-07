import { DefaultQuestionsCls } from '../../utils/types';
import MediumCard from '../medium_card';
import Question from '../question';
import styles from './index.module.css';


type props = {
    className?: string;
    questions: DefaultQuestionsCls[];
};

function WelcomMessage(props: props) {
    return (
        <MediumCard innerClassName={styles.card + ' ' + (props.className ? props.className : '')}>
            <h1>What information can I help you digest today?</h1>
            <div className={styles.randomQuestions}>
                {props.questions.map((question, index) => {
                    return <Question question={question} className={styles.question} key={'question-' + index}></Question>
                })}
            </div>
        </MediumCard>
    )
};

export default WelcomMessage;
