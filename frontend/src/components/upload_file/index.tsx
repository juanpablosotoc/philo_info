import { PropsWithChildren, useRef } from 'react';
import styles from './index.module.css';
import upload_white from '../../SVG/icons/upload_white.svg';
import upload_grey from '../../SVG/icons/upload_grey.svg';
import UploadedFiles from '../uploaded_files';

type Props = PropsWithChildren<{
    className?: string;
    files: Array<File>;
    setFiles: React.Dispatch<React.SetStateAction<Array<File>>>;
}>


function UploadFile(props: Props) {
    const input = useRef<HTMLInputElement>(null);
    const handleClick = () => {
        input.current!.click();
    }
    function handleChange (event: React.ChangeEvent<HTMLInputElement>) {
        if (input.current!.files) {
            props.setFiles((prevValue) => {
             return [...prevValue, ...Array.from(input.current!.files!)]   
    })
    }}
    return (
        <div className={`${props.className ? props.className : ''} ${styles.wrapper}`}>
            <UploadedFiles files={props.files} setFiles={props.setFiles}></UploadedFiles>
            <button className={styles.btn} onClick={handleClick}>
                <svg width="24" height="24" viewBox="0 0 24 24" className={styles.uploadFileIcon} fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="#2F2F2F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M17 8L12 3L7 8" stroke="#2F2F2F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 3V15" stroke="#2F2F2F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Upload file</span>
            </button>
            <input type="file" ref={input} multiple hidden className={`${styles.input} ${props.className ? props.className : ''}`} onChange={handleChange}/>
        </div>
    );
}

export default UploadFile;
