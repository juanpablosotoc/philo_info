import { useEffect, useRef, useState } from 'react';
import styles from './index.module.css';

type props = {
    className?: string;
    label: string;
    value: string;
    setValue: (value: string) => void;
}

function LongTextInput(props: props) {
    const wrapper = useRef<HTMLDivElement>(null);
    const input = useRef<HTMLTextAreaElement>(null);
    function setHeight() {
        input.current!.style.height = "0px";
        input.current!.style.height = (input.current!.scrollHeight - 26) + "px";
        if (input.current!.scrollHeight > 130) {
            wrapper.current!.style.height = "130px";
            wrapper.current!.style.overflowY = "scroll";
        } else {
            wrapper.current!.style.height = (input.current!.scrollHeight) + "px";
            wrapper.current!.style.overflowY = "hidden";
        };
    };
    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        props.setValue(event.target.value);
        setHeight();
    };
    useEffect(() => {
        setHeight();
    });
    useEffect(() => {
        if (props.value.length) wrapper.current!.classList.add(styles.active)
        else wrapper.current!.classList.remove(styles.active);
    }, [props.value])
  return (
    <div className={`${styles.wrapper} ${props.className ? props.className : ''}`} ref={wrapper}>
      <textarea className={styles.input} placeholder={props.label} value={props.value} onChange={handleChange} ref={input}/>
    </div>
  );
}

export default LongTextInput;
