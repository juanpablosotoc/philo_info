import { OutputTypes } from "../../utils/types";
import eye from '../../SVG/icons/eye_open.svg';

type props = {
    className?: string;
    type: OutputTypes;
}

function OutputTypeCard(props: props) {
  return (
    <div>
        <img src={eye} alt="" />
        <p>{props.type}</p>
    </div>
  );
};

export default OutputTypeCard;
