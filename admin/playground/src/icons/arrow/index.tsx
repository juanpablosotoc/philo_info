import styles from './styles.module.css';

interface Props {
    className?: string;
    tailClassName?: string;
}

export default function Arrow(props: Props) {
    return (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className={(props.className ? props.className : '') + ' ' + styles.arrow}>
<g clip-path="url(#clip0_301_520)">
<path d="M12.34 0.527203C11.5759 -0.175734 10.3371 -0.175734 9.57305 0.527203C8.80898 1.23014 8.80898 2.36986 9.57305 3.07279L12.34 0.527203ZM22.0435 12L23.4269 13.2728C24.191 12.5699 24.191 11.4302 23.4269 10.7272L22.0435 12ZM9.57305 20.9273C8.80898 21.6303 8.80898 22.7698 9.57305 23.4728C10.3371 24.1757 11.5759 24.1757 12.34 23.4728L9.57305 20.9273ZM9.57305 3.07279L20.6601 13.2728L23.4269 10.7272L12.34 0.527203L9.57305 3.07279ZM20.6601 10.7272L9.57305 20.9273L12.34 23.4728L23.4269 13.2728L20.6601 10.7272Z" fill="black"/>
<path d="M2 12L22 12" className={styles.tail + ' ' + (props.tailClassName ? props.tailClassName : '')} stroke="black" stroke-width="3" stroke-linecap="round"/>
</g>
<defs>
<clipPath id="clip0_301_520">
<rect width="24" height="24" fill="white"/>
</clipPath>
</defs>
</svg>

    )
};

