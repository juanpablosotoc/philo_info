import ShortTextInput from "../../components/short_text_input";
import PasswordInput from "../../components/password_input";
import SubmitBtn from "../../components/submit_btn";
import OrLine from "../../components/or_line";
import OAuth from "../../components/oauth";
import Footer from "../../components/footer";
import black_anaglyphic_logo from '../../SVG/logo/black_anaglyphic.svg';
import styles from './index.module.css';
import {Link, Form, redirect, useSearchParams, useRouteError} from "react-router-dom";
import {getToken, post, saveToken} from "../../utils/http";
import { useEffect, useState } from "react";
import { ErrorType } from "../../utils/types";
import { Helmet } from 'react-helmet';

type props = {
    type: "login" | "signup"
}

// const location = useLocation();
// const error = new URLSearchParams(location.search).get("error");

function LoginSignup (props: props) {
    let error_message;
    let welcome_message;
    let invitation_message;
    let error = (useRouteError() as ErrorType);
    const [searchParams, setSearchParams] = useSearchParams();
    if (error) {
        error_message = error.statusText;
    } else {
        error_message = searchParams.get("error") as string;
    }
    if (props.type === "login") {
        welcome_message = <h1>Welcome back</h1>
        invitation_message = <p>Don't have an account? <Link to='/signup'>Sign up</Link></p>
    }
    else {
        welcome_message = <h1>Create an account</h1>
        invitation_message = <p>Already have an account? <Link to='/login'>Log in</Link></p>
    };
    if (error_message) {
        welcome_message = <h1>{error_message}</h1>
    };
    useEffect(() => {
        setSearchParams({}); // Clear the error message
    }, []);
    const [email, setEmail] = useState('');
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
                    <ShortTextInput value={email} setValue={setEmail} name="email"/>
                    <PasswordInput name="password"/>
                    <SubmitBtn label="Continue" />
                </Form>
                {invitation_message}
                <OrLine />
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
    if (token && token.length > 0) {
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
