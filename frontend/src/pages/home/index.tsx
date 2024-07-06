import { redirect } from "react-router-dom";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import { clearOAuth, fetch_, getOAuth, getToken, saveToken, post_stream } from "../../utils/http";
import { InformationBundleCls, MessageCls, DefaultQuestionsCls, 
    ThreadCls, StreamMessageResponse, StreamMessageResponseMetadata,
    StreamMessageResponseChoices, StreamMessageResponseProcessedInfo } from "../../utils/types";
import { useEffect, useRef, useState } from "react";
import Messages from "../../components/messages";
import { Helmet } from "react-helmet";
import { getFormData } from "../../utils/functions";
import SideMenu from "../../components/side_menu";


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
    useEffect(() => {
        if(jwt_is_ready) {
            fetch_("mixed/topics_threads", true, "GET", "application/json", "alt_token" , (jsonResp) => {
                console.log(jsonResp);
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

    async function handleSubmit() {
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
        // Make a post request to the server
        const body_obj = {links, texts, questions}
        const body = getFormData(body_obj);
        const resp = post_stream("threads/message", true, body)
        for await (let list of resp) {
            for (let item of (list as Array<StreamMessageResponse>)) {
                if (item.type === 'metadata') {
                    setMessages((prevMessages) => {
                        return prevMessages.map((prevMessage) => {
                            if (!prevMessage.id) {
                                prevMessage.id = item.message_id;
                                prevMessage.threadId = (item as StreamMessageResponseMetadata).thread_id;
                            }
                            return prevMessage;
                        });
                    });
                    const thread = new ThreadCls(item.thread_id, item.thread_name, new Date());
                    setThreads((prevThreads) => {
                        return [...prevThreads, thread];
                    });
                } else if (item.type === 'choices') {
                    setMessages((prevMessages) => {
                        return prevMessages.map((prevMessage) => {
                            if (prevMessage.id === item.message_id) {
                                prevMessage.possible_outputs = (item as StreamMessageResponseChoices).possible_outputs;
                            }
                            return prevMessage;
                    })});
                } else {
                    // Type is processed_info
                    setMessages((prevMessages) => {
                        return prevMessages.map((prevMessage) => {
                            if (prevMessage.id === item.message_id) {
                                prevMessage.processedInfos.push({id: (item as StreamMessageResponseProcessedInfo).id, info: (item as StreamMessageResponseProcessedInfo).info});
                            }
                            return prevMessage;
                        });
                    })
                }
            }
        }
    };
    return (
        <div className={styles.wrapper}>
            <Helmet>
                <title>Home | FacTic</title>
            </Helmet>
            <Messages messages={messages} questions={questions} className={styles.messages}></Messages>
            <div className={styles.fixedWrapper}>
                <div className={styles.inputWrapper}>
                    <UploadFile className={styles.uploadFile} files={files} setFiles={setFiles}/>
                    <LongTextInput myRef={longTextInput} label="Enter information" className={styles.longTextInput} value={longTextInputValue} setValue={setLongTextInputValue}/>
                    <SubmitBtn className={styles.submit_btn} theme='dark' onClick={handleSubmit}/>
                </div>
                <div className={styles.blurryModal} ref={blurryModal}></div>
                <SideMenu className={styles.sideMenu} type="threads" data={threads} myRef={sideMenuElement} active="home"></SideMenu>
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
