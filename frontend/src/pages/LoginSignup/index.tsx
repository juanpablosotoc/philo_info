import ShortTextInput from "../../components/short_text_input";
import PasswordInput from "../../components/password_input";
import SubmitBtn from "../../components/submit_btn";
import OrLine from "../../components/or_line";
import OAuth from "../../components/oauth";
import Footer from "../../components/footer";
import black_anaglyphic_logo from '../../SVG/logo/black_v3.svg';
import styles from './index.module.css';
import { Form, redirect, useSearchParams, useRouteError} from "react-router-dom";
import {getOAuth, getToken, post, saveToken} from "../../utils/http";
import { useEffect, useState } from "react";
import { ErrorType } from "../../utils/types";
import { Helmet } from 'react-helmet';
import MyLink from "../../components/my_link";


type props = {
    type: "login" | "signup"
}

function LoginSignup (props: props) {
    let error_message;
    let welcome_message;
    let invitation_message;
    const [email, setEmail] = useState('');
    let error = (useRouteError() as ErrorType);
    const [searchParams, setSearchParams] = useSearchParams();
    if (error) {
        error_message = error.statusText;
    } else {
        error_message = searchParams.get("error") as string;
    }
    if (props.type === "login") {
        welcome_message = <h1 className={styles.welcomeMessage}>Welcome back</h1>
        invitation_message = <p>Don't have an account? <MyLink to='/signup'>Sign up</MyLink></p>
    }
    else {
        welcome_message = <h1 className={styles.welcomeMessage}>Create an account</h1>
        invitation_message = <p>Already have an account? <MyLink to='/login'>Log in</MyLink></p>
    };
    if (error_message) {
        welcome_message = <h1 className={styles.welcomeMessage}>{error_message}</h1>
    };
    useEffect(() => {
        setSearchParams({}); // Clear the error message
        document.body.style.backgroundColor = "var(--main_white)";
    }, []);
    const title = props.type[0].toUpperCase() + props.type.slice(1) + ' | Factic';
    return (
        <>
        <Helmet>
            <title>{title}</title>
        </Helmet>
        <div className={styles.wrapper}>
            <img src={black_anaglyphic_logo} alt="Factic logo" />
            <div className={styles.formWrapper}>
                {welcome_message}
                <Form method="post">
                    <ShortTextInput type={'email'}  color="white" value={email} setValue={setEmail} name="email"/>
                    <PasswordInput name="password"/>
                    <SubmitBtn label="Continue" theme="light" />
                </Form>
                {invitation_message}
                <OrLine className={styles.orLine}/>
                <OAuth type="apple" />
                <OAuth type="google" />
                <OAuth type="microsoft" />
            </div>
            <Footer />
        </div>
        </>
    )
};

export async function loader() {
    const token = getToken();
    const oauth = getOAuth();
    if ((token && token.length > 0) || (oauth.identity && oauth.provider)) {
        return redirect("/")
    };
    return null;
}

export async function signupAction({ params, request }: any) {
    try {
        const formData = await request.formData();
        const sendData = {
            email: formData.get("email"),
            password: formData.get("password"),
        };
        const data = await post("users/create_user", false, sendData);
        const token = data.token;
        saveToken(token);
        return redirect("/");
    } catch (e) {
        return redirect("/signup?error=" + (e as ErrorType).statusText);
    }
};

export async function loginAction({ params, request }: any) {
    try {
        const formData = await request.formData();
        const sendData = {
            email: formData.get("email"),
            password: formData.get("password"),
        };
        const data = await post("users/login", false, sendData);
        const token = data.token;
        saveToken(token);
        return redirect("/");
    } catch (e) {
        return redirect("/login?error=" + (e as ErrorType).statusText);
    }
};

export default LoginSignup;
