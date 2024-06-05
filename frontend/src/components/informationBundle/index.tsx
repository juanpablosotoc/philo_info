import { InformationBundleCls } from '../../utils/types';
import styles from './index.module.css';
import Link from '../link';
import Text from '../text';
import UploadedFiles from '../uploaded_files';
import addWhite from '../../SVG/icons/add_white.svg';
import addGrey from '../../SVG/icons/add_grey.svg';
import IconBtn from '../iconBtn';
import Files from '../files';

type Props = {
    className?: string;
    informationBundle: InformationBundleCls;
    myRef?: any;
}

function InformationBundle(props: Props) {
    return (
        <div className={`${props.className ? props.className : ''} ${styles.wrapper}`} ref={props.myRef}>
            <IconBtn iconSrc={addWhite} altText='add icon' className={styles.addIcon} ></IconBtn>
            <div className={styles.informationBundle}>
                {props.informationBundle.text ? <Text text={props.informationBundle.text}></Text> : ''}
                {props.informationBundle.link.length ? <Link link={props.informationBundle.link}></Link> : ''}
                {props.informationBundle.files.length ? <Files files={props.informationBundle.files}></Files> : ''}
            </div>
        </div>
    )
};

export default InformationBundle;