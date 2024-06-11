import styles from './index.module.css';


function Lines() {
    const lines = [];
    for (let i = 0; i < 25; i++) {
        lines.push(<hr key={'line' + i} className={styles.line} style={{marginTop: 20 - (i*.9), height: i+1}}></hr>);
    }
    return (
        <div className={styles.wrapper}>
            {lines}
        </ div>
    );
};

export default Lines;
