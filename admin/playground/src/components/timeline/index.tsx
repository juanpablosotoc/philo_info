import React from 'react';
import styles from './styles.module.css';

export default function Timeline(props: React.PropsWithChildren<{}>) {
  return (
    <div className={styles.timeline}>
      <div className={styles.innerWrapper}>
      {React.Children.map(props.children, (child, index) => {
          return (
          <div className={styles.eventWrapper + ' ' + (index === 0 ? styles.active : '')}>
            {child}
          </div>
          )
        })}
      </div>
    </div>
  );
}