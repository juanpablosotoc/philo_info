import { LongTextInputType } from '../../utils/types';
import SmallCardGroup from '../small_card_group';
import styles from './index.module.css';


type Props = {
    className?: string;
    links: Array<string>;
}
function Links(props: Props) {
    let linkTexts = [];
    for (let i = 0; i < props.links.length; i++) {
        let linkDisplayText = props.links[i];
        if (linkDisplayText.length > 30) linkDisplayText = linkDisplayText.slice(0, 27) + '...';
        linkTexts.push(linkDisplayText);
    }
    return (
        <SmallCardGroup smallCardLabels={linkTexts} label='Links' smallCardClassName={styles.link}></SmallCardGroup>
    )
};

export default Links;
