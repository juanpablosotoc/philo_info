import SmallCard from '../small_card';
import styles from './index.module.css';


type Props = {
    className?: string;
    label: string;
    handleXClick?: any;
    smallCardLabels: string[];
    smallCardClassName?: string;
};

function SmallCardGroup(props: Props) {
    return (
        <div className={props.className ? props.className : ''}>
            <p  className={styles.label}>{props.label}</p>
            {props.smallCardLabels.map((label, index) => {
                return props.handleXClick ? (
                <SmallCard key={index} label={label} handleXClick={props.handleXClick} className={props.smallCardClassName ? props.smallCardClassName : ''}/>
                 ) : (
                 <SmallCard key={index} label={label} className={props.smallCardClassName ? props.smallCardClassName : ''}/>
                 )
            })}
        </div>
    )
};

export default SmallCardGroup;
