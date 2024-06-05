import { useLoaderData, redirect } from "react-router-dom";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import ShortTextInput from "../../components/short_text_input";
import Circles from "../../components/circles";
import OutputChoiceCard from "../../components/output_choice_card";
import { get, getToken, post } from "../../utils/http";
import { InformationBundleCls, MessageCls, QuestionCls, Topic } from "../../utils/types";
import Modal from "../../components/modal";
import { useEffect, useState } from "react";
import Threads from "../../components/threads";
import { useThreads } from "../../utils/hooks";
import Messages from "../../components/messages";
import { Helmet } from "react-helmet";

function Home () {
    const [currentMessage, setCurrentMessage] = useState(1);
    const [topicHasChanged, setTopicHasChanged] = useState(false);
    const [threadActive, setThreadActive] = useState(false);
    const [topic, setTopic] = useState('');
    const { topic: topic_, questions: questions_} = useLoaderData() as Topic;
    const {threads, error, isLoading} = useThreads();
    const [longTextInputValue, setLongTextInputValue] = useState('');
    const [files, setFiles] = useState<Array<File>>([]);
    const [messages, setMessages] = useState<Array<MessageCls>>([]);
    useEffect(()=>{
        const explainQuestions = questions_.map((question) => '/explain ' + question);
        setTopic(topic_);
        setMessages(explainQuestions.map((question) => {
            return new MessageCls(new QuestionCls(question), "question")}));
    }, []);
    async function handleFocusOutTopic () {
        if (!topicHasChanged) return;
        setTopicHasChanged(false);
        const json = await post("topics/", false, {topic: topic});
        setMessages(json.questions.map((question : any) => {
            return new MessageCls(new QuestionCls('/explain ' + question), "question")}
        ));
    }
    function handleSubmit() {
        if (!longTextInputValue.trim() && !files.length) return;
        setThreadActive(true);
        const text = longTextInputValue.startsWith('http') ? '' : longTextInputValue;
        const link = longTextInputValue.startsWith('http') ? longTextInputValue : '';
        let message = new MessageCls(new InformationBundleCls(text, files, link), "informationBundle");
        setMessages((prevMessages) => {
            return [...prevMessages, message];
        });
        setLongTextInputValue('');
        setFiles([]);
    };
    let topicInputClassname = '';
    if (threadActive) topicInputClassname = styles.hidden;
    return (
        <>
        <Helmet>
            <title>Home | Factic</title>
        </Helmet>
        <Modal topBottom="top"></Modal>
        <Messages messages={messages} setCurrentMessage={setCurrentMessage}></Messages>
        <Modal topBottom="bottom"></Modal>
        <div className={styles.wrapper}>
            <div className={styles.upperWrapper}>
                <Threads threads={threads} className={styles.threads} isLoading={isLoading} error={error}/>
                <div className={styles.topicQuestionWrapper}>
                    <ShortTextInput name="text" label="Topic" value={topic} setValue={setTopic} handleFocusOut={handleFocusOutTopic} setTopicHasChanged={setTopicHasChanged} className={topicInputClassname}/>
                    <Circles number={messages.length} filledNumber={currentMessage}/>
                </div>
                <div className={styles.outputWrapper}>
                    <OutputChoiceCard types={["text", "speech", "timeline"]} className={styles.output_choice + ' ' + styles.first} third={true}/>
                    <OutputChoiceCard types={["text", "speech", "timeline"]} className={styles.output_choice + ' ' + styles.middle}/>
                    <OutputChoiceCard types={["text", "speech", "timeline"]} className={styles.output_choice + ' ' + styles.last} first={true}/>
                </div>
            </div>
            <div className={styles.inputWrapper}>
                <UploadFile className={styles.uploadFile} files={files} setFiles={setFiles}/>
                <LongTextInput label="Enter information" className={styles.longTextInput} value={longTextInputValue} setValue={setLongTextInputValue}/>
                <SubmitBtn className={styles.submit_btn} onClick={handleSubmit}/>
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
