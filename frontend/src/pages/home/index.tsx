import { useLoaderData, redirect, useLocation } from "react-router-dom";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import { clearOAuth, fetch_, getOAuth, getToken, post, saveToken } from "../../utils/http";
import { InformationBundleCls, MessageCls, QuestionCls, Thread, Topic } from "../../utils/types";
import Modal from "../../components/modal";
import { useEffect, useState } from "react";
import Threads from "../../components/threads";
import Messages from "../../components/messages";
import { Helmet } from "react-helmet";
import TopFrame from "../../components/top_frame";
import {LongTextInputType} from "../../utils/types";


function Home () {
    // If the jwt is ready, we can fetch the topic
    const [jwt_is_ready, setJwtIsReady] = useState(false);
    const [threads, setThreads] = useState<Thread[]>([]);
    const [longTextInputValue, setLongTextInputValue] = useState<Array<LongTextInputType>>([]);
    const [files, setFiles] = useState<Array<File>>([]);
    const [messages, setMessages] = useState<Array<MessageCls>>([]);
    const [questions, setQuestions] = useState<Array<QuestionCls>>([]);
    useEffect(() => {
        if(jwt_is_ready) {
            fetch_("mixed/topics_threads", true, "GET", "application/json", "alt_token" , (jsonResp) => {
                setThreads(jsonResp.threads);
                const questions = jsonResp.topics_questions.map((topic_question : any) => {
                    return new QuestionCls('/explain ' + topic_question.question, topic_question.topic)}
                );
                setQuestions(questions);
            });
        }
     }, [jwt_is_ready]);
    useEffect(()=>{
        document.body.style.backgroundColor = "var(--shades_black_100)";
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

    function handleSubmit() {
        const texts = longTextInputValue.filter((value) => value.type === 'text').map((value) => value.content);
        const links = longTextInputValue.filter((value) => value.type === 'link').map((value) => value.content);
        let message = new MessageCls(new InformationBundleCls(texts, files, links), "informationBundle");
        setMessages((prevMessages) => {
            return [...prevMessages, message];
        });
        setLongTextInputValue([]);
        setFiles([]);
    };
    return (
        <div className={styles.wrapper}>
            <Helmet>
                <title>Home | Factic</title>
            </Helmet>
            <TopFrame active="home"></TopFrame>
            <Modal topBottom="top"></Modal>
            <Messages messages={messages} questions={questions} className={styles.messages}></Messages>
            <Modal topBottom="bottom"></Modal>
            <div className={styles.fixedWrapper}>
                <div className={styles.inputWrapper}>
                    <UploadFile className={styles.uploadFile} files={files} setFiles={setFiles}/>
                    <LongTextInput label="Enter information" className={styles.longTextInput} value={longTextInputValue} setValue={setLongTextInputValue}/>
                    <SubmitBtn className={styles.submit_btn} theme='dark' onClick={handleSubmit}/>
                </div>
                <Threads threads={threads} className={styles.threads}/>
            </div>
        </div>
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
