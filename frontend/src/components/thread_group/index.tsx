import { ThreadCls } from '../../utils/types';
import SmallCardGroup from '../small_card_group';

type Props = {
    className?: string;
    threads: ThreadCls[];
    date?:string;
}

function ThreadGroup (props: Props) {
    const threadLabels = props.threads.map((thread, index) => thread.name);
    if (!threadLabels.length) {
        threadLabels.push('New thread');
    }
    return (
        <SmallCardGroup label={props.date ? props.date : 'Today'} smallCardLabels={threadLabels}></SmallCardGroup>
    )
};

export default ThreadGroup;