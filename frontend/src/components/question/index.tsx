import { useEffect, useRef } from 'react';
import styles from './index.module.css';

type Props = {
    className?: string;
    question: string;
    questionNumber: number;
    setQuestionNumber: React.Dispatch<React.SetStateAction<number>>;
}

function Question(props: Props) {
    const element = useRef<HTMLParagraphElement>(null);

    useEffect(() => {
        const observer = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) props.setQuestionNumber(props.questionNumber + 1);
        });
          observer.observe( element.current!);
        }
    , []);
    return (
        <p className={styles.question} ref={element}>{props.question}</p>
    )
};

export default Question;