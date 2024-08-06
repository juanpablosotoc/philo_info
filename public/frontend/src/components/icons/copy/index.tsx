import styles from './styles.module.css';


function Copy() {
    return <svg className={styles.icon} width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g clip-path="url(#clip0_524_220)">
    <path d="M16 7H4C2.34315 7 1 8.34315 1 10V22C1 23.6569 2.34315 25 4 25H16C17.6569 25 19 23.6569 19 22V10C19 8.34315 17.6569 7 16 7Z" stroke="black" stroke-width="2" stroke-miterlimit="10"/>
    <path d="M19 19H22C23.66 19 25 17.66 25 16V4C25 2.34 23.66 1 22 1H10C8.34 1 7 2.34 7 4V7" stroke="black" stroke-width="2" stroke-miterlimit="10"/>
    </g>
    <defs>
    <clipPath id="clip0_524_220">
    <rect width="26" height="26" fill="white"/>
    </clipPath>
    </defs>
    </svg>      
};

export default Copy;