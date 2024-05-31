import ShortTextInput from "../../components/short_text_input";
import PasswordInput from "../../components/password_input";
import SubmitBtn from "../../components/submit_btn";
import OrLine from "../../components/or_line";
import OAuth from "../../components/oauth";
import Footer from "../../components/footer";
import black_anaglyphic_logo from '../../SVG/logo/black_anaglyphic.svg';
import styles from './index.module.css';
import {Link} from "react-router-dom";

type props = {
    type: "login" | "signup"
}

function LoginSignup (props: props) {
    let welcome_message;
    let invitation_message;
    if (props.type === "login") {
        welcome_message = <h1>Welcome back</h1>
        invitation_message = <p>Don't have an account? <Link to='/signup'>Sign up</Link></p>
    }
    else {
        welcome_message = <h1>Create an account</h1>
        invitation_message = <p>Already have an account? <Link to='/login'>Log in</Link></p>
    };
    return (
        <div className={styles.wrapper}>
            <img src={black_anaglyphic_logo} alt="Factic logo" />
            <div className={styles.formWrapper}>
                {welcome_message}
                <ShortTextInput />
                <PasswordInput />
                <SubmitBtn />
                {invitation_message}
                <OrLine />
                <OAuth type="apple" />
                <OAuth type="google" />
                <OAuth type="microsoft" />
            </div>
            <Footer />
        </div>
    )
};

export default LoginSignup;
