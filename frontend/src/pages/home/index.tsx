import { redirect } from "react-router-dom";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import { clearOAuth, fetch_, getOAuth, getToken, saveToken, post_stream } from "../../utils/http";
import { MessageCls, DefaultQuestionsCls, 
    ThreadCls, RequestMessageCls} from "../../utils/types";
import { useEffect, useRef, useState } from "react";
import Messages from "../../components/messages";
import { Helmet } from "react-helmet";
import SideMenu from "../../components/side_menu";
import HandleSubmitCls from "./functions";

function Home () {
    const longTextInput = useRef<HTMLDivElement>(null);
    const sideMenuElement = useRef<HTMLDivElement>(null);
    const blurryModal = useRef<HTMLDivElement>(null);
    // If the jwt is ready, we can fetch the topic
    const [jwt_is_ready, setJwtIsReady] = useState(false);
    const [threads, setThreads] = useState<ThreadCls[]>([]);
    const [longTextInputValue, setLongTextInputValue] = useState<string>('');
    const [files, setFiles] = useState<Array<File>>([]);
    const [messages, setMessages] = useState<Array<MessageCls>>([]);
    const [questions, setQuestions] = useState<Array<DefaultQuestionsCls>>([]);
    const handleSubmitObj = new HandleSubmitCls(longTextInput, setLongTextInputValue, setFiles, longTextInputValue, files, setMessages, setThreads);
    useEffect(() => {
        if(jwt_is_ready) {
            fetch_("mixed/topics_threads", true, "GET", "application/json", "alt_token" , (jsonResp) => {
                setThreads(jsonResp.threads.map((thread: any) => {
                    return new ThreadCls(thread.id, thread.name, new Date(thread.date));
                }
                ));
                const questions = jsonResp.topics_questions.map((topic_question : any) => {
                    return new DefaultQuestionsCls('/explain ' + topic_question.question, topic_question.topic)}
                );
                setQuestions(questions);
            });
        }
     }, [jwt_is_ready]);
    useEffect(()=>{
        const testMessages: Array<MessageCls> = [];
        const message = new MessageCls('other', new RequestMessageCls('Hello', 'Sure! Did you know that the worlds oldest known tree is a Great Basin bristlecone pine (Pinus longaeva) located in Californias White Mountains? Its estimated to be over 5,000 years old! This tree has witnessed human history from ancient civilizations to modern times. Its fascinating how nature can offer such remarkable longevity and resilience.'), 1, 1);
        testMessages.push(message);testMessages.push(message);testMessages.push(message);testMessages.push(message);testMessages.push(message);
        testMessages.push(message);
        testMessages.push(message);
        testMessages.push(message);
        testMessages.push(message);
        testMessages.push(message);
        testMessages.push(message);
        setMessages(testMessages);
        // set the document background color to black
        document.documentElement.style.backgroundColor = "var(--shades_black_150)";
        document.body.style.backgroundColor = "var(--shades_black_150)";
        document.getElementById("root")!.style.backgroundColor = "var(--shades_black_150)";
        const token = getToken();
        if(token) setJwtIsReady(true);
        else {
            const body = JSON.stringify({access_token: getOAuth().identity, provider: getOAuth().provider});
            fetch_("oauth/login_create_account", false, "POST", "application/json", "access_token", (jsonResp) => {
                saveToken(jsonResp.token);
                setJwtIsReady(true);
            }, undefined, ()=>{
                clearOAuth();
            }, body);
        }
        sideMenuElement.current!.onmouseenter = () => {
            blurryModal.current!.classList.add(styles.active);
        }
        sideMenuElement.current!.onmouseleave = () => {
            blurryModal.current!.classList.remove(styles.active);
        }
    }, []);
    return (
        <div className={styles.wrapper}>
            <Helmet>
                <title>Home | FacTic</title>
            </Helmet>
            <SideMenu className={styles.sideMenu} type="threads" data={threads} myRef={sideMenuElement} active="home"></SideMenu>
            <div className={styles.right}>
                <Messages messages={messages} questions={questions} className={styles.messages}></Messages>
                <div className={styles.inputWrapper}>
                    <UploadFile className={styles.uploadFile} files={files} setFiles={setFiles}/>
                    <LongTextInput myRef={longTextInput} label="Enter information" className={styles.longTextInput} value={longTextInputValue} setValue={setLongTextInputValue}/>
                    <SubmitBtn className={styles.submit_btn} theme='dark' onClick={handleSubmitObj.handleSubmit}/>
                </div>
            </div>
            <div className={styles.blurryModal} ref={blurryModal}></div>
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
