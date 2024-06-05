import { useEffect, useRef } from 'react';
import styles from './index.module.css';

type Props = {
    className?: string;
    question: string;
    questionNumber: number;
    setQuestionNumber: React.Dispatch<React.SetStateAction<number>>;
    myRef?: any;
}

function Question(props: Props) {
    return (
        <>
            {props.myRef ? (
            <p className={`${styles.question} ${props.className ? props.className : ''}`} ref={props.myRef}>{props.question}</p>
        ) : (
            <p className={`${styles.question} ${props.className ? props.className : ''}`}>{props.question}</p>
        )}
        </>
    )
};

export default Question;