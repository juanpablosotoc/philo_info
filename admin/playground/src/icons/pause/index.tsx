import styles from './styles.module.css';

interface Props {
    className?: string;
}


export default function Pause(props: Props) {
    return (
        <svg className={styles.icon + ' ' + (props.className ? props.className : '')} width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M3.16667 0C2.85725 0 2.5605 0.126428 2.34171 0.351472C2.12292 0.576515 2 0.88174 2 1.2V22.8C2 23.1183 2.12292 23.4235 2.34171 23.6485C2.5605 23.8736 2.85725 24 3.16667 24H7.5C7.80942 24 8.10617 23.8736 8.32496 23.6485C8.54375 23.4235 8.66667 23.1183 8.66667 22.8V1.2C8.66667 0.88174 8.54375 0.576515 8.32496 0.351472C8.10617 0.126428 7.80942 0 7.5 0H3.16667ZM16.5 0C16.1906 0 15.8938 0.126428 15.675 0.351472C15.4563 0.576515 15.3333 0.88174 15.3333 1.2V22.8C15.3333 23.1183 15.4563 23.4235 15.675 23.6485C15.8938 23.8736 16.1906 24 16.5 24H20.8333C21.1428 24 21.4395 23.8736 21.6583 23.6485C21.8771 23.4235 22 23.1183 22 22.8V1.2C22 0.88174 21.8771 0.576515 21.6583 0.351472C21.4395 0.126428 21.1428 0 20.8333 0H16.5Z" fill="black"/>
</svg>

    )
};

