import Question from "../question";
import styles from './index.module.css';


type Props = {
    questions: string[];
    className?: string;
    setCurrentQuestion: React.Dispatch<React.SetStateAction<number>>;
}

function Questions (props: Props) {
    return (
        <>
            {props.questions.map((question, index) =>{
            return (
                <>
                <Question question={question} setQuestionNumber={props.setCurrentQuestion} questionNumber={index} key={index + 'question'}></Question>
                {index < (props.questions.length -1) ? <br className={styles.br} key={index + 'br'}/> : ''}
                </>
            )
            })}
        </>
    )
};

export default Questions;
