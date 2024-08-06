import styles from './index.module.css';
import SmallCard from '../small_card';
import FilePreviewWindow from '../filePreviewWindow';

type Props = {
    files : File[];
    setFiles?: React.Dispatch<React.SetStateAction<File[]>>;
}

function UploadedFiles(props: Props) {
    function handleClick(e: React.MouseEvent<HTMLDivElement>) {
        const index = Array.from(e.currentTarget.parentElement!.parentElement!.children).indexOf(e.currentTarget.parentElement!);
        props.setFiles!((prevValue) => {
            const newFiles = [...prevValue];
            newFiles.splice(index, 1);
            return newFiles;
        });
    };
    return (
        <div className={styles.wrapper}>
            {props.files.length ? props.files.map((file, index) => {
                // const newName = file.name.length > 6 ? file.name.slice(0, 6) + '...' : file.name;
                return (
                    // <SmallCard key={`file-${index}`} label={newName} handleXClick={handleClick}></SmallCard>
                    <FilePreviewWindow file={file}></FilePreviewWindow>
                )
            }) : null}
        </div>
    )
};

export default UploadedFiles;
