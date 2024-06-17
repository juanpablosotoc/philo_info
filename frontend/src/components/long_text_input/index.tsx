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
        // delete all child nodes that are <br>
        let usefulNode;
        for (let i = childNodes.length - 1; i >= 0; i--) {
            const childNode = childNodes[i];
            if (childNode.nodeName === 'SPAN') {
                break; // Exit the loop if the last node is a <span>
            }
            if (childNode.nodeType !== 3) continue;
            if (childNode.textContent === '\n') {
                continue;
            }
            if (!childNode.textContent!.trim()) continue;
            usefulNode = childNode;
            break;
        }
        if (!usefulNode) return;
        const lastTextNode = usefulNode.textContent;
        const words = lastTextNode?.trim().split(' ');
        const lastTextInputed = words?.pop();
        // It fails because last text node is empty
        console.log(event.target.childNodes)
        if (!lastTextInputed) {
            return;
        };
        if (isLink(lastTextInputed)) {
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
            usefulNode.textContent = '';
            // Add the span element to the wrapper
            wrapper.current?.insertBefore(spanElement, usefulNode);
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
