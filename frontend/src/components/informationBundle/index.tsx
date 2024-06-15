import { InformationBundleCls } from '../../utils/types';
import styles from './index.module.css';
import Link from '../link';
import Text from '../text';
import Files from '../files';

type Props = {
    className?: string;
    informationBundle: InformationBundleCls;
    myRef?: any;
}

function InformationBundle(props: Props) {
    return (
        <div className={`${props.className ? props.className : ''} ${styles.wrapper}`} ref={props.myRef}>
            {/* The add icon */}
            <svg width="24" className={styles.icon} height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19" stroke="#F7F7F7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M5 12H19" stroke="#F7F7F7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <div className={styles.informationBundle}>
                {props.informationBundle.text ? <Text text={props.informationBundle.text}></Text> : ''}
                {props.informationBundle.link.length ? <Link link={props.informationBundle.link}></Link> : ''}
                {props.informationBundle.files.length ? <Files files={props.informationBundle.files}></Files> : ''}
            </div>
        </div>
    )
};

export default InformationBundle;