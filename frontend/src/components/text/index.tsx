import styles from './index.module.css';
import SmallCardGroup from '../small_card_group';

type Props = {
    text: string;
}

function Text(props: Props) {
    let innerText = props.text.trim();
    if(innerText.length > 300) innerText = innerText.slice(0, 297) + '...';
    return (
        <SmallCardGroup label='Text' smallCardClassName={styles.text} smallCardLabels={[innerText]}></SmallCardGroup>
    )
};

export default Text;
