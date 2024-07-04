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
    const handleChange = (event: React.ChangeEvent<HTMLDivElement>) => {
        // set the value of the input
        props.setValue(event.target.textContent? event.target.textContent : '');
        const childNodes = event.target.childNodes;
        let lastNode = childNodes[childNodes.length - 1];
        if (!lastNode) return;
        // Get rid of all the br, empty text nodes and div elements
        let checkedNode = lastNode;
        while (checkedNode) {
            const prevSibling = checkedNode.previousSibling!;
            if (checkedNode.nodeName === 'BR' || (checkedNode.nodeName === '#text' && !checkedNode.textContent) || (checkedNode.nodeName === 'SPAN' && !checkedNode.textContent)
            || (checkedNode.nodeName === 'DIV' && !(checkedNode as HTMLDivElement).innerHTML)) {
                props.myRef.current?.removeChild(checkedNode);
            }
            checkedNode = prevSibling;
        }
        lastNode = childNodes[childNodes.length - 1];
        if (!lastNode) return;
        const lastTextNode = lastNode.textContent;
        const words = lastTextNode?.trim().split(/[  ]/g);
        // It fails because last text node is empty
        if (!words?.length) return;
        // check if event was backspace
        const wasBackspace = (event.nativeEvent as InputEvent).inputType === 'deleteContentBackward';
        let removeTextContent = false;
        let newTextContent = '';
        if (!wasBackspace) {
            for (let word of words) {
                if (isLink(word)) {
                    removeTextContent = true;
                    const spanElement = document.createElement('span');
                    spanElement.contentEditable = 'false';
                    spanElement.className = styles.link;
                    spanElement.innerText = word;
                    // Add the span element to the wrapper
                    props.myRef.current?.insertBefore(spanElement, lastNode);
                } else {
                    newTextContent = newTextContent ? newTextContent.concat(' ', word) : word;
                }
            };
        }
        if (removeTextContent && lastNode) {
            // Remove the text content
            lastNode.textContent = newTextContent;
        }
        // if last node is div make sure to add a br element into the div
        if (lastNode.nodeName === 'DIV' && !(lastNode as HTMLDivElement).innerHTML) {
            const brElement = document.createElement('br');
            lastNode.appendChild(brElement);
        }
    };
    useEffect(() => {
        if (props.value.length) props.myRef.current!.classList.add(styles.active)
        else {
            props.myRef.current!.classList.remove(styles.active);
            props.myRef.current!.innerHTML = '';
        }
    }, [props.value])
  return (
    <div contentEditable onInput={handleChange} className={styles.input + ' ' + (props.className ? props.className : '')} ref={props.myRef}>
    </div>
  );
}

export default LongTextInput;
