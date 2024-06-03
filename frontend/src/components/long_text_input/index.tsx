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
        if (event.target.value.length) input.current!.classList.add(styles.active)
        else input.current!.classList.remove(styles.active);
        setValue(event.target.value);
    };

  return (
    <div className={`${styles.wrapper} ${props.className ? props.className : ''}`}>
      <textarea className={styles.input} placeholder={props.label} value={value} onChange={handleChange} ref={input}/>
    </div>
  );
}

export default LongTextInput;
