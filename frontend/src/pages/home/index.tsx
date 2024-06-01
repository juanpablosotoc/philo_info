import { useLoaderData, redirect } from "react-router-dom";
import { getToken } from "../../utils/http";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import ShortTextInput from "../../components/short_text_input";
import Circles from "../../components/circles";

function Home () {
    return (
        <div>
            <div>
                <ShortTextInput name="text" label="Topic"/>
                <div>
                    <div className={styles.questionWrapper}>
                        <p>Question?</p>
                        <Circles number={5}/>
                    </div>
                    <div className={styles.outputWrapper}>

                    </div>
                </div>
            </div>
            <div className={styles.inputWrapper}>
                <UploadFile />
                <LongTextInput label="Enter information" className={styles.longTextInput}/>
                <SubmitBtn />
            </div>
        </div>
    )
};

export async function loader() {
    const token = getToken();
    if (!token || token.length === 0) {
        return redirect("/login")
    };
    // get threads!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return null;
  }

export default Home;
