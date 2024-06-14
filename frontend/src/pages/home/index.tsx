import { useLoaderData, redirect, useLocation } from "react-router-dom";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import ShortTextInput from "../../components/short_text_input";
import Circles from "../../components/circles";
import OutputChoiceCard from "../../components/output_choice_card";
import { clearOAuth, fetch_, getOAuth, getToken, post, saveToken } from "../../utils/http";
import { InformationBundleCls, MessageCls, QuestionCls, Thread, Topic } from "../../utils/types";
import Modal from "../../components/modal";
import { useEffect, useState } from "react";
import Threads from "../../components/threads";
import Messages from "../../components/messages";
import { Helmet } from "react-helmet";


function Home () {
    // The message that is currently being displayed
    const [currentMessage, setCurrentMessage] = useState(1);
    // If the topic has changed, we need to update the questions
    const [topicHasChanged, setTopicHasChanged] = useState(false);
    // If the thread is active, we need to hide the topic input
    const [threadActive, setThreadActive] = useState(false);
    // If the jwt is ready, we can fetch the topic
    const [jwt_is_ready, setJwtIsReady] = useState(false);
    const [topic, setTopic] = useState('');
    const [threads, setThreads] = useState<Thread[]>([]);
    const [longTextInputValue, setLongTextInputValue] = useState('');
    const [files, setFiles] = useState<Array<File>>([]);
    const [messages, setMessages] = useState<Array<MessageCls>>([]);
    useEffect(() => {
        if(jwt_is_ready) {
            fetch_("mixed/topics_threads", true, "GET", "application/json", "alt_token" , (jsonResp) => {
                setThreads(jsonResp.threads);
                const topic = jsonResp.topic_questions.topic
                const questions = jsonResp.topic_questions.questions.map((question : any) => {
                    return new MessageCls(new QuestionCls('/explain ' + question), "question")}
                );
                setTopic(topic);
                setMessages(questions);
            });
        }
     }, [jwt_is_ready]);
    useEffect(()=>{
        document.body.style.backgroundColor = "var(--main_white)";
        const token = getToken();
        if(token) setJwtIsReady(true);
        else {
            fetch_("oauth/login_create_account", false, "POST", "application/json", "access_token", (jsonResp) => {
                saveToken(jsonResp.token);
                setJwtIsReady(true);
            }, undefined, ()=>{
                clearOAuth();
            }, JSON.stringify({access_token: getOAuth().identity, provider: getOAuth().provider}));
        }

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
                <Threads threads={threads} className={styles.threads}/>
                <div className={styles.topicQuestionWrapper}>
                    <ShortTextInput name="text" type="text" color="black" label="Topic" value={topic} setValue={setTopic} handleFocusOut={handleFocusOutTopic} setTopicHasChanged={setTopicHasChanged} className={topicInputClassname}/>
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
    const oauth = getOAuth();
    // If there is no oauth then get your jwt token
    if (!(oauth.identity && oauth.provider)) {
        const token = getToken();
        // If neither the oauth or jwt token exist, redirect to login
        if (!token || token.length === 0) {
            return redirect("/login")
        };
    };
    return null;
  }

export default Home;
