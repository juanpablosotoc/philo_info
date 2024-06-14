import styles from './index.module.css';
import chevron_grey from '../../SVG/icons/chevron_grey.svg';
import chevron_white from '../../SVG/icons/chevron_white.svg';
import settingsIcon from '../../SVG/icons/settings.svg';
import writeIcon from '../../SVG/icons/write.svg';
import { Thread } from '../../utils/types';
import ThreadGroup from '../thread_group';
import { dateComparison } from '../../utils/functions';
import IconBtn from '../iconBtn';
import Chevron from '../chevron';

type Props = {
    threads: Thread[];
    // isLoading: boolean;
    className?: string;
    // error: boolean;
};

interface ThreadGroupsInterface {
    'Today': Thread[];
    'This month': Thread[];
    'Older': Thread[];
}

function Threads({ threads, className}: Props) {
    const threadGroups: ThreadGroupsInterface = {
        'Today': [],
        'This month': [],
        'Older': [],
    };
    for (let thread of threads) {
        threadGroups[dateComparison(thread.date)].push(thread);
    }
    let threadGroupElements = Object.entries(threadGroups).map(([threadGroup, threads]) => (
        threads.length ? <ThreadGroup key={threadGroup} date={threadGroup} threads={threads} /> : undefined
    ));
    threadGroupElements = threadGroupElements.filter((element) => element !== undefined);
    if (!threadGroupElements.length) {
        threadGroupElements.push(<ThreadGroup date='Today' threads={[]}></ThreadGroup>);
    };
    return (
        <div className={`${styles.wrapper} ${className}`}>
            <div className={styles.threadsWrapper}>
                <div>
                    <div className={styles.iconsWrapper}>
                        <IconBtn altText='settings icon' iconSrc={settingsIcon}></IconBtn>
                        <IconBtn iconSrc={writeIcon} altText='add icon'></IconBtn>
                    </div>
                    {threadGroupElements}
                </div>
            </div>
            <div className={styles.chevronWrapperWrapper}>
                <div className={styles.chevronWrapper}>
                    <Chevron className={styles.chevron} stemClassName={styles.chevronStem}/>
                </div>
            </div>
        </div>
    );
}

export default Threads;
