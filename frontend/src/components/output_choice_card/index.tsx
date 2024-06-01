import { OutputTypes } from '../../utils/types';
import styles from './index.module.css';
import OutputTypeCard from '../output_type_card';

type Props = {
    className?: string;
    types: Array<OutputTypes>;
};

function OutputChoiceCard (props: Props) {
    return (
        <div>
            <p>Explain with:</p>
            <hr />
            {props.types.map((type, index) => {
                return <OutputTypeCard key={index} type={type} />
            })}
        </div>
    )
};

export default OutputChoiceCard;
