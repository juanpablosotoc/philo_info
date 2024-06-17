import { useLoaderData, redirect, useLocation } from "react-router-dom";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import { clearOAuth, fetch_, getOAuth, getToken, post, saveToken } from "../../utils/http";
import { InformationBundleCls, LongTextInputType, MessageCls, DefaultQuestionsCls, Thread, Topic } from "../../utils/types";
import Modal from "../../components/modal";
import { useEffect, useRef, useState } from "react";
import Threads from "../../components/threads";
import Messages from "../../components/messages";
import { Helmet } from "react-helmet";
import TopFrame from "../../components/top_frame";
import { isLink } from "../../utils/functions";


function Home () {
    const longTextInput = useRef<HTMLDivElement>(null);
    // If the jwt is ready, we can fetch the topic
    const [jwt_is_ready, setJwtIsReady] = useState(false);
    const [threads, setThreads] = useState<Thread[]>([]);
    const [longTextInputValue, setLongTextInputValue] = useState<string>('');
    const [files, setFiles] = useState<Array<File>>([]);
    const [messages, setMessages] = useState<Array<MessageCls>>([]);
    const [questions, setQuestions] = useState<Array<DefaultQuestionsCls>>([]);
    useEffect(() => {
        if(jwt_is_ready) {
            fetch_("mixed/topics_threads", true, "GET", "application/json", "alt_token" , (jsonResp) => {
                setThreads(jsonResp.threads);
                const questions = jsonResp.topics_questions.map((topic_question : any) => {
                    return new DefaultQuestionsCls('/explain ' + topic_question.question, topic_question.topic)}
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
        let texts: Array<string> = [];
        const links: Array<string> = [];
        for (let node of longTextInput.current!.childNodes) {
            // if node is span add the text content
            if (node.nodeName === 'SPAN') {
                links.push(node.textContent!);
            } else if (node.nodeName === '#text') {
                if (texts.length) {
                    texts[texts.length - 1] = texts[texts.length - 1] + ' ' + node.textContent!;
                } else if (node.textContent && node.textContent.trim()){
                    texts.push(node.textContent!);
                }
            }
        };
        const questions = texts.filter((text) => {
            return text.startsWith('/explain');
        });
        texts = texts.filter((text) => {
            return !text.startsWith('/explain');
        });
        let message = new MessageCls(new InformationBundleCls(texts, files, links, questions));
        setMessages((prevMessages) => {
            return [...prevMessages, message];
        });
        setLongTextInputValue('');
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
                    <LongTextInput myRef={longTextInput} label="Enter information" className={styles.longTextInput} value={longTextInputValue} setValue={setLongTextInputValue}/>
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
