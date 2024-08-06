import styles from './styles.module.css';
import timelineStyles from '../timeline/styles.module.css';


import React, { useEffect, useRef, useState } from 'react';


interface Props {
    date: string;
}

export default function TimelineEvent(props: React.PropsWithChildren<Props>) {
  const dateRef = useRef<HTMLParagraphElement>(null);
  const timelineEventRef = useRef<HTMLDivElement>(null);
  React.useEffect(() => {
    if (dateRef.current) {
      const measuredWidth = dateRef.current.offsetWidth;
      // set css variable dateWidth to the width of the date element
        timelineEventRef.current!.style.setProperty('--dateWidth', measuredWidth + 'px');
    }
  }, [dateRef]);

  const handleActive = () => {
    // Remove active class from all other events
    document.querySelectorAll('.' + timelineStyles.active).forEach((element) => {
      element.classList.remove(timelineStyles.active);
    });

    // Add active class to the current events parent (the parent is found in the timeline component)
    timelineEventRef.current!?.parentElement?.classList.add(timelineStyles.active);
  };

  return (
    <div className={styles.timelineEvent} ref={timelineEventRef}>
      <button onClick={handleActive} className={styles.dateButton}>
        <p ref={dateRef} className={styles.date}>{props.date}</p>
      </button>
      <div className={styles.content}>{props.children}</div>
    </div>
  );
}
