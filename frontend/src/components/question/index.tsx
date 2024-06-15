import styles from './index.module.css';

type Props = {
    className?: string;
    question: string;
}

function Question(props: Props) {
    return (
        <div className={styles.wrapper}>
            {/* A camera icon */}
            <svg width="24" height="25" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M23 19.5C23 20.0304 22.7893 20.5391 22.4142 20.9142C22.0391 21.2893 21.5304 21.5 21 21.5H3C2.46957 21.5 1.96086 21.2893 1.58579 20.9142C1.21071 20.5391 1 20.0304 1 19.5V8.5C1 7.96957 1.21071 7.46086 1.58579 7.08579C1.96086 6.71071 2.46957 6.5 3 6.5H7L9 3.5H15L17 6.5H21C21.5304 6.5 22.0391 6.71071 22.4142 7.08579C22.7893 7.46086 23 7.96957 23 8.5V19.5Z" stroke="#05F3DB" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M12 17.5C14.2091 17.5 16 15.7091 16 13.5C16 11.2909 14.2091 9.5 12 9.5C9.79086 9.5 8 11.2909 8 13.5C8 15.7091 9.79086 17.5 12 17.5Z" stroke="#05F3DB" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <p className={`${styles.question} ${props.className ? props.className : ''}`}>{props.question}</p>
        </div>
    )
};

export default Question;