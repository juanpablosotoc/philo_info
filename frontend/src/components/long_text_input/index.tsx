import { useRef, useState } from 'react';
import styles from './index.module.css';

type props = {
    className?: string;
    label: string;
}

function LongTextInput(props: props) {

    const [value, setValue] = useState('');
    const input = useRef<HTMLTextAreaElement>(null)
    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        if (event.target.value.length) {
            input.current!.className += ` ${styles.active}`;
        } else {
            input.current!.className = styles.input + ` ${props.className ? props.className : ''}`;
        };
        setValue(event.target.value);
    };

  return (
      <textarea className={`${styles.input} ${props.className ? props.className : ''}`} placeholder={props.label} value={value} onChange={handleChange} ref={input}/>
  );
}

export default LongTextInput;
