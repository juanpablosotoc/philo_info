import styles from './styles.module.css';
import React from 'react';

export default function Video(props: React.PropsWithChildren<{title: string}>) {
    return (
        <div className={styles.video}>
            <div className={styles.metadata}>
                <p className={styles.title}>{props.title}</p>
            </div>
            <div className={styles.content}>{props.children}</div>
        </div>
    );
}