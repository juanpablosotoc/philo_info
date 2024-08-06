import styles from './styles.module.css';


interface Props {
    className?: string;
}

function Book(props: Props) {
    return <svg width="24" className={styles.icon + ' ' + (props.className ? props.className : '')} height="28" viewBox="0 0 24 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M5.59 20.59C5.22 20.95 5 21.45 5 22C5 23.1 5.9 24 7 24H22C23.1 24 24 24.9 24 26C24 26.55 23.78 27.05 23.41 27.41C23.05 27.78 22.55 28 22 28H2C0.9 28 0 27.1 0 26V2.45C0 1.1 1.1 0 2.45 0H9.79C11.15 0 12.24 1.1 12.24 2.45V6.91C12.24 7.31 12.79 7.51 13.11 7.23L15.37 5.21C15.82 4.81 16.54 4.82 16.98 5.21L19.22 7.21C19.53 7.5 20.08 7.3 20.08 6.89V1.75C20.08 0.78 20.87 0 21.83 0H22.25C23.22 0 24 0.78 24 1.75V18.34C24 19.26 23.26 20 22.34 20H7C6.45 20 5.95 20.22 5.59 20.59Z" fill="#F7F7F7"/>
    </svg>      
};

export default Book;
