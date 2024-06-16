import { useEffect, useRef, useState } from 'react';
import styles from './index.module.css';
import { LongTextInputType } from '../../utils/types';

type props = {
    className?: string;
    label: string;
    value: Array<LongTextInputType>;
    setValue: React.Dispatch<React.SetStateAction<Array<LongTextInputType>>>;
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
        const stringInputs = event.target.value.split(' ');
        if (!stringInputs.length) return props.setValue([]);
        let type: 'text' | 'link' = 'text';
        if (stringInputs.at(-1)!.startsWith('http') || stringInputs.at(-1)!.startsWith('https')) type = 'link';
        const newValue: LongTextInputType = {type: type, content: stringInputs[-1]};
        props.setValue((prevValue) => {
            return [...prevValue, newValue];
        });
        setHeight();
    };
    useEffect(() => {
        setHeight();
    });
    useEffect(() => {
        if (props.value.length) wrapper.current!.classList.add(styles.active)
        else wrapper.current!.classList.remove(styles.active);
    }, [props.value])
    let textareaValue = '';
    props.value.forEach((element) => {
        textareaValue = textareaValue.concat(element.content);
    });
  return (
    <div className={`${styles.wrapper} ${props.className ? props.className : ''}`} ref={wrapper}>
      <textarea className={styles.input} placeholder={props.label} value={textareaValue} onChange={handleChange} ref={input}/>
    </div>
  );
}

export default LongTextInput;
