import { PropsWithChildren, useRef } from 'react';
import styles from './index.module.css';
import upload_white from '../../SVG/icons/upload_white.svg';
import upload_grey from '../../SVG/icons/upload_grey.svg';


type Props = PropsWithChildren<{
    className?: string;
}>


function UploadFile(props: Props) {
    const input = useRef<HTMLInputElement>(null);
    return (
        <div>
            <button className={styles.btn}>
                <div className={styles.uploadDiv}>
                    <img src={upload_white} alt="upload icon" className={styles.whiteUpload} />
                    <img src={upload_grey} alt="upload icon" className={styles.greyUpload} />
                </div>
                <span>Upload file</span>
            </button>
            <input type="file" ref={input} hidden className={`${styles.input} ${props.className ? props.className : ''}`}/>
        </div>
    );
}

export default UploadFile;
