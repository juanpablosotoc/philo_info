import React from 'react';
import styles from './styles.module.css';

export default function Timeline(props: React.PropsWithChildren<{}>) {
  return (
    <div className={styles.timeline}>
        {props.children}
    </div>
  );
}