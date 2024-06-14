import { OutputTypes } from '../../utils/types';
import styles from './index.module.css';
import OutputTypeCard from '../output_type_card';
import React, { useRef } from 'react';
import { getXYPercentages } from '../../utils/functions';

type Props = {
    className?: string;
};

function MediumCard (props: React.PropsWithChildren<Props>) {
    const wrapper = useRef<HTMLDivElement>(null);
    function handleHover(e: any) {
        const { xPercent, yPercent } = getXYPercentages(e, wrapper.current);
        wrapper.current!.style.background = `radial-gradient(circle at ${xPercent}% ${yPercent}%, var(--mixed_primary_white), var(--main_white) 70%)`;
        let x;
        let y;
        x = (yPercent - 50) / 5;
        y = (xPercent - 50) / 5;
        y /= -4;
        x /= 4;
        console.log(x, 'x', y, 'y');
        wrapper.current!.style.transform = `translateY(-50%) perspective(500px) rotateY(${y}deg) rotateX(${x}deg)`;
    };
    function handleLeave() {
        wrapper.current!.style.transform = `translateY(-50%) perspective(500px) rotateY(0deg) rotateX(0deg)`;
    }
    return (
        <div className={`${styles.medium_card} ${props.className ? props.className : ''}`} ref={wrapper} onMouseMove={handleHover} onMouseLeave={handleLeave}>
            {props.children}
        </div>
    )
};

export default MediumCard;
