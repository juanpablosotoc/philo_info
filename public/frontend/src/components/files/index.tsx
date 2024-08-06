import styles from './index.module.css';
import SmallCardGroup from '../small_card_group';


type Props = {
    files: File[];
};

function Files(props: Props) {
    let file_names: string[] = [];
    if(props.files.length)file_names = props.files.map((file, index) => file.name.length > 20 ? file.name.slice(0, 17) + '...' : file.name);
    return (
        <SmallCardGroup smallCardLabels={file_names} label='Files' smallCardClassName={styles.innerFiles} className={styles.files}></SmallCardGroup>
    )
};

export default Files;
