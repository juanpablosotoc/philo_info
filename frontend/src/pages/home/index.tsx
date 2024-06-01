import { useLoaderData, redirect } from "react-router-dom";
import { getToken } from "../../utils/http";
import UploadFile from "../../components/upload_file";
import LongTextInput from "../../components/long_text_input";
import SubmitBtn from "../../components/submit_btn";
import styles from './index.module.css';
import ShortTextInput from "../../components/short_text_input";
import Circles from "../../components/circles";
import OutputChoiceCard from "../../components/output_choice_card";

function Home () {
    return (
        <div className={styles.wrapper}>
            <div className={styles.upperWrapper}>
                <ShortTextInput name="text" label="Topic"/>
                <div className={styles.questionOutputWrapper}>
                    <div className={styles.questionWrapper}>
                        <p>Question?</p>
                        <Circles number={5} filledNumber={2}/>
                    </div>
                    <div className={styles.outputWrapper}>
                        <OutputChoiceCard types={["text", "speech", "timeline"]}/>
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
