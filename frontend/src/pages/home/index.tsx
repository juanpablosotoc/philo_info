import { useLoaderData, redirect } from "react-router-dom";
import { getToken, post } from "../../utils/http";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import ShortTextInput from "../../components/short_text_input";
import Circles from "../../components/circles";
import OutputChoiceCard from "../../components/output_choice_card";
import { get } from "../../utils/http";
import { Topic } from "../../utils/types";
import Modal from "../../components/modal";
import { useEffect, useState } from "react";
import Question from "../../components/question";
import Questions from "../../components/questions";

function Home () {
    const [currentQuestion, setCurrentQuestion] = useState(1);
    const [topicHasChanged, setTopicHasChanged] = useState(false);
    const [questions, setQuestions] = useState<Array<string>>([]);
    const [topic, setTopic] = useState('');
    const { topic: topic_, questions: questions_} = useLoaderData() as Topic;
    useEffect(()=>{
        setQuestions(questions_);
        setTopic(topic_);
    }, []);
    async function handleFocusOutTopic () {
        if (!topicHasChanged) return;
        setTopicHasChanged(false);
        const json = await post("topics/", false, {topic: topic});
        setQuestions(json.questions)
    }
    return (
        <>
        <Modal topBottom="top"></Modal>
        <Questions questions={questions} setCurrentQuestion={setCurrentQuestion}></Questions>
        <Modal topBottom="bottom"></Modal>
        <div className={styles.wrapper}>
            <div className={styles.upperWrapper}>
                <div className={styles.topicQuestionWrapper}>
                    <ShortTextInput name="text" label="Topic" value={topic} setValue={setTopic} handleFocusOut={handleFocusOutTopic} setTopicHasChanged={setTopicHasChanged}/>
                    <Circles number={questions.length} filledNumber={currentQuestion}/>
                </div>
                <div className={styles.outputWrapper}>
                    <OutputChoiceCard types={["text", "speech", "timeline"]} className={styles.output_choice + ' ' + styles.first} third={true}/>
                    <OutputChoiceCard types={["text", "speech", "timeline"]} className={styles.output_choice + ' ' + styles.middle}/>
                    <OutputChoiceCard types={["text", "speech", "timeline"]} className={styles.output_choice + ' ' + styles.last} first={true}/>
                </div>
            </div>
            <div className={styles.inputWrapper}>
                <UploadFile className={styles.uploadFile}/>
                <LongTextInput label="Enter information" className={styles.longTextInput}/>
                <SubmitBtn className={styles.submit_btn} />
            </div>
        </div>
        </>
    )
};

export async function loader() {
    const token = getToken();
    if (!token || token.length === 0) {
        return redirect("/login")
    };
    const json = await get("topics/") as Topic;
    return json;
  }

export default Home;
