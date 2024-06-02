import { OutputTypes } from '../../utils/types';
import styles from './index.module.css';
import OutputTypeCard from '../output_type_card';
import { useRef } from 'react';
import { getXYPercentages } from '../../utils/functions';

type Props = {
    className?: string;
    types: Array<OutputTypes>;
    first?: boolean;
};

function OutputChoiceCard (props: Props) {
    const outputChoiceCardClass = 'output_choice_card';
    let initialRotateY = -45;
    let initialRotateX = 20;
    const wrapper = useRef<HTMLDivElement>(null);
    function handleHover(e: any) {
        const card = e.target.closest('.output_choice_card');
        const { xPercent, yPercent } = getXYPercentages(e, card);
        wrapper.current!.style.background = `radial-gradient(circle at ${xPercent}% ${yPercent}%, var(--mixed_primary_black), var(--main_black) 70%)`;
        let x;
        let y;
        x = (yPercent - 50) / 5;
        y = (xPercent - 50) / 5;
        x *= -1;
        y *= -1;
        let translate = '';
        if (!props.first) translate = 'translateX(70%)';
        wrapper.current!.style.transform = `rotateY(${ initialRotateY + y}deg) rotateX(${ initialRotateX + x}deg) ${translate}`;
    };
    function handleLeave() {
        wrapper.current!.style.transform = `rotateY(${initialRotateY}deg) rotateX(${initialRotateX}deg) translateX(0)`;
    }
    return (
        <div className={`${styles.wrapper} ${outputChoiceCardClass} ${props.className ? props.className : ''}`} ref={wrapper} onMouseMove={handleHover} onMouseLeave={handleLeave}>
            <p>Explain with:</p>
            <div className={styles.choices}>
            {props.types.map((type, index) => {
                return <OutputTypeCard key={index} type={type} />
            })}
            </div>
        </div>
    )
};

export default OutputChoiceCard;
