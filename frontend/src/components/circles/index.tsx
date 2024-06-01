import styles from './index.module.css';

type props = {
    className?: string;
    number: number;
}

function Circles(props: props) {
    const circles = [];
    for (let i = 0; i < props.number; i++) {
        circles.push(<div key={i} className={styles.circle}></div>);
    }
    return (
        <div className={styles.circles}>
            {circles}
        </div>
    );
};

export default Circles;
