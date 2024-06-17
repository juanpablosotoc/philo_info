import { useEffect, useRef, useState } from 'react';
import styles from './index.module.css';
import { LongTextInputType } from '../../utils/types';

type props = {
    className?: string;
    label: string;
    value: Array<LongTextInputType>;
    setValue: React.Dispatch<React.SetStateAction<Array<LongTextInputType>>>;
}

function isLink(text: string) {
    return text.startsWith('http://') || text.startsWith('https://');
};

function LongTextInput(props: props) {
    const wrapper = useRef<HTMLDivElement>(null);
    const handleChange = (event: React.ChangeEvent<HTMLDivElement>) => {
        const childNodes = event.target.childNodes;
        let lastNode = childNodes[childNodes.length - 1];
        if (!lastNode) return;
        const prevNode = lastNode.previousSibling;
        const prevPrevNode = prevNode?.previousSibling;
        if (prevNode) {
            if (prevNode.nodeName === 'BR') {
                wrapper.current?.removeChild(prevNode);
                wrapper.current?.removeChild(lastNode);
                lastNode = prevPrevNode!;
            };
        };
        const lastTextNode = lastNode.textContent;
        const words = lastTextNode?.trim().split(' ');
        const lastTextInputed = words?.pop();
        // It fails because last text node is empty
        console.log(event.target.childNodes)
        if (!lastTextInputed) {
            return;
        };
        // check if event was backspace
        const wasBackspace = (event.nativeEvent as InputEvent).inputType === 'deleteContentBackward';
        if (!wasBackspace && isLink(lastTextInputed)) {
            console.log('is link')
            props.setValue((prevValue) => {
                return [...prevValue, {type: 'link', content: lastTextInputed}];
            });
            console.log('creating new element')
            // Insert a span element to make the link clickable
            const spanElement = document.createElement('span');
            spanElement.contentEditable = 'false';
            spanElement.className = styles.link;
            spanElement.innerText = lastTextInputed;
            // Del the text from the div
            lastNode.textContent = '';
            // Add the span element to the wrapper
            wrapper.current?.insertBefore(spanElement, lastNode);
        }
        else {
            props.setValue((prevValue) => {
                if (!prevValue.length) return [{type: 'text', content: lastTextInputed}];
                const lastElement = prevValue[prevValue.length - 1];
                if (lastElement.type === 'text') {
                    prevValue[prevValue.length - 1].content = lastElement.content.concat(lastTextInputed);
                    return prevValue;
                }
                return [...prevValue, {type: 'text', content: lastTextInputed}];
            });
        }
    };
    useEffect(() => {
        if (props.value.length) wrapper.current!.classList.add(styles.active)
        else wrapper.current!.classList.remove(styles.active);
    }, [props.value])
    let textareaValue = '';
    props.value.forEach((element) => {
        textareaValue = textareaValue.concat(element.content);
    });
  return (
    <div contentEditable onInput={handleChange} className={styles.input + ' ' + (props.className ? props.className : '')} ref={wrapper}>
    </div>
  );
}

export default LongTextInput;
