import SmallCardGroup from '../small_card_group';
import styles from './index.module.css';


type Props = {
    className?: string;
    link: string;
}
function Link(props: Props) {
    let linkText = props.link.trim();
    if (linkText.length > 30) linkText = linkText.slice(0, 27) + '...';
    return (
        <SmallCardGroup smallCardLabels={[linkText]} label='Links' smallCardClassName={styles.link}></SmallCardGroup>
    )
};

export default Link;
