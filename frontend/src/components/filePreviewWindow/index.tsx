import { fetch_raw, post } from '../../utils/http';
import styles from './styles.module.css';


interface Props {
    className?: string;
    file: File;
}

function FilePreviewWindow (props: Props) {
    
    return (
        <img className={(props.className ? props.className : '') + ' ' + styles.preview} src="" alt="preview of file uploaded" />
    )
};

export default FilePreviewWindow;
