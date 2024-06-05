import styles from './index.module.css';
import chevron_grey from '../../SVG/icons/chevron_grey.svg';
import chevron_white from '../../SVG/icons/chevron_white.svg';
import settingsIcon from '../../SVG/icons/settings.svg';
import writeIcon from '../../SVG/icons/write.svg';
import { Thread } from '../../utils/types';
import ThreadGroup from '../thread_group';
import { dateComparison } from '../../utils/functions';
import IconBtn from '../iconBtn';

type Props = {
    threads: Thread[];
    isLoading: boolean;
    className?: string;
    error: boolean;
};

interface ThreadGroupsInterface {
    'Today': Thread[];
    'This month': Thread[];
    'Older': Thread[];
}

function Threads({ threads, isLoading, error, className}: Props) {
    const threadGroups: ThreadGroupsInterface = {
        'Today': [],
        'This month': [],
        'Older': [],
    };
    if (!error) {
        for (let thread of threads) {
            threadGroups[dateComparison(thread.date)].push(thread);
        }
    }
    let threadGroupElements = Object.entries(threadGroups).map(([threadGroup, threads]) => (
        !error && threads.length ? <ThreadGroup key={threadGroup} date={threadGroup} threads={threads} /> : undefined
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
            <div className={styles.chevronWrapper}>
                <img src={chevron_grey} alt="chevron" className={styles.greyChevron + ' ' + styles.chevron} />
                <img src={chevron_white} alt="chevron" className={styles.whiteChevron + ' ' + styles.chevron} />
            </div>
        </div>
    );
}

export default Threads;
