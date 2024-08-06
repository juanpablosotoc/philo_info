import { InfoMessageCls } from "../../utils/types";

interface Props {
    infoBundle: InfoMessageCls;
    className ?: string;
}


function InfoBundle (props: Props) {
    return (
        <div className={props.className ? props.className : ''}></div>
    )
};

export default InfoBundle;