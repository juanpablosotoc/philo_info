import { OutputTypes } from "../../utils/types";
import camera from '../../SVG/icons/camera.svg';

type props = {
    className?: string;
    type: OutputTypes;
}

function OutputTypeCard(props: props) {
  return (
    <div>
        <img src={camera} alt="" />
        <p>{props.type}</p>
    </div>
  );
};

export default OutputTypeCard;
