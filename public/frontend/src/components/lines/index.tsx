import { useRef } from 'react';
import styles from './index.module.css';
import useOnScreen from '../../utils/hooks';

function Lines() {
    const lines = [];
    for (let i = 0; i < 28; i++) {
        lines.push(<hr key={'line' + i} className={styles.line} style={{marginTop: 20 - (i*.8), height: i+1}}></hr>);
    }
    const wrapper = useRef<HTMLDivElement>(null);
    const onScreen = useOnScreen(wrapper);
    // If the element is on screen, set the background color to black
    if (onScreen) {
        document.documentElement.style.backgroundColor = 'var(--shades_black_200)';
    } else {
        document.documentElement.style.backgroundColor = "var(--main_white)";
    }
    return (
        <div className={styles.wrapper} ref={wrapper}>
            {lines}
        </ div>
    );
};

export default Lines;
