import React from 'react';
import styles from './styles.module.css';

export default function Sequence(props: React.PropsWithChildren<{}>) {
    const [currentBar, setCurrentBar] = React.useState(0);
    function handleClick(index: number) {
        setCurrentBar(index);
    }
    return (
    <div className={styles.sequence}>
        {/* for every child add a bar */ React.Children.map(props.children, (child, index) => {
            return (
                <div className={styles.innerWrapper + ' ' + (currentBar === index ? styles.active : (index < currentBar ? styles.prevActive : ''))}>
                    <div className={styles.bar} onClick={(e)=>{handleClick(index)}}></div>
                    <div className={styles.sequencewrapper}>
                        {child}
                    </div>
                </div>
            )
        })}
    </div>
    )
}