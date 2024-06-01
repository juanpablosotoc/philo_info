import styles from './index.module.css';

type props = {
    className?: string;
    number: number;
    filledNumber: number;
}

function Circles(props: props) {
    const circles = [];
    for (let i = 0; i < props.number; i++) {
        let className;
        if (i === props.filledNumber - 1) className = styles.filledCircle
        else className = styles.donut;
        const element = <div key={i} className={className}></div>;
        circles.push(element);
    }
    return (
        <div className={styles.circles}>
            {circles}
        </div>
    );
};

export default Circles;
