import styles from './index.module.css';
import SmallCardGroup from '../small_card_group';
import { LongTextInputType } from '../../utils/types';

type Props = {
    texts: Array<string>;
}

function Texts(props: Props) {
    let displayTexts =[];
    for (let i = 0; i < props.texts.length; i++) {
        let text = props.texts[i];
        if (text.length > 300) text = text.slice(0, 297) + '...';
        displayTexts.push(text);
    }
    return (
        <SmallCardGroup label='Text' smallCardClassName={styles.text} smallCardLabels={displayTexts}></SmallCardGroup>
    )
};

export default Texts;
