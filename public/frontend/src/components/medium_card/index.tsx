import styles from './index.module.css';
import React, { useEffect, useRef } from 'react';
import { getXYPercentages } from '../../utils/functions';
import ai2 from '../../images/ai2.jpg';
import ai3 from '../../images/ai3.jpg';
import ai4 from '../../images/ai4.jpg';
import ai9 from '../../images/ai9.jpg';
import ai10 from '../../images/ai10.jpg';
import ai14 from '../../images/ai14.jpg';
import ai15 from '../../images/ai15.jpg';
import ai16 from '../../images/ai16.jpg';


type Props = {
    innerClassName?: string;
};

function MediumCard (props: React.PropsWithChildren<Props>) {
    const possible_images = [ai2, ai3, ai4, ai9, ai10, ai14, ai15, ai16];
    const images = [useRef<HTMLImageElement>(null), useRef<HTMLImageElement>(null)]
    const wrapper = useRef<HTMLDivElement>(null);
    function handleHover(e: any) {
        const { xPercent, yPercent } = getXYPercentages(e, wrapper.current);
        let x;
        let y;
        x = (yPercent - 50) / 5;
        y = (xPercent - 50) / 5;
        y /= -4;
        x /= 4;
        wrapper.current!.style.transform = `translateY(-50%) perspective(400px) rotateY(${y}deg) rotateX(${x}deg)`;
    };
    function handleLeave() {
        wrapper.current!.style.transform = `translateY(-50%) perspective(400px) rotateY(0deg) rotateX(0deg)`;
    }
    useEffect(() => {
        const num = Math.floor(Math.random() * possible_images.length);
        const current_img = possible_images[num];
        images.forEach((image) => {
            image.current!.src = current_img;
    })}, []);
    return (
        <div className={`${styles.medium_card}`} ref={wrapper} onMouseMove={handleHover} onMouseLeave={handleLeave}>
            <div className={styles.imgWrapper}>
                <img ref={images[0]} className={styles.underlyingImage} alt="desktop vibrant wallpaper image" />
            </div>
            <div className={styles.modal}></div>
            <div className={styles.innerWrapper}>
                <div className={styles.imgWrapper}>
                    <img ref={images[1]} className={styles.topImage} alt="desktop vibrant wallpaper image" />
                </div>
                <div className={styles.children + ' ' + (props.innerClassName ? props.innerClassName : '')}>
                    {props.children}
                </div>
            </div>
        </div>
    )
};

export default MediumCard;
