import { PropsWithChildren, useRef, useState } from 'react';
import styles from './index.module.css';
import upload_white from '../../SVG/icons/upload_white.svg';
import upload_grey from '../../SVG/icons/upload_grey.svg';
import UploadedFiles from '../uploaded_files';
import ImgHover from '../imgHover';

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
                <ImgHover img={upload_grey} imgHover={upload_white} imgClassName={styles.greyUpload} hoverClassName={styles.whiteUpload} altText='upload icon'></ImgHover>
                <span>Upload file</span>
            </button>
            <input type="file" ref={input} multiple hidden className={`${styles.input} ${props.className ? props.className : ''}`} onChange={handleChange}/>
        </div>
    );
}

export default UploadFile;
