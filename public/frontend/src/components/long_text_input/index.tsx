import { useEffect, useRef, useState } from 'react';
import styles from './index.module.css';
import { LongTextInputType } from '../../utils/types';
import { isLink } from '../../utils/functions';

type props = {
    className?: string;
    label: string;
    value: string;
    myRef: any;
    setValue: React.Dispatch<React.SetStateAction<string>>;
}


function LongTextInput(props: props) {
    function handleChange(e: React.FormEvent<HTMLSpanElement>) {
        // get the elements text
        const text = e.currentTarget.innerText.replace('\n', '');
        if (text) {
            e.currentTarget.classList.add(styles.active)
        } else {
            e.currentTarget.classList.remove(styles.active)
        }
    }
  return (
    <span className={styles.input + ' ' + (props.className ? props.className : '')} role="textbox" contentEditable onInput={handleChange}></span>
  );
}

export default LongTextInput;
