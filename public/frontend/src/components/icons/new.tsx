
interface Props {
    className?: string;
    crossLineClassName?: string;
}

function New(props: Props) {
    return <svg className={props.className ? props.className : ''} width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g clip-path="url(#clip0_396_230)">
    <path d="M20.5556 1H3.44444C2.09441 1 1 2.09441 1 3.44444V20.5556C1 21.9056 2.09441 23 3.44444 23H20.5556C21.9056 23 23 21.9056 23 20.5556V3.44444C23 2.09441 21.9056 1 20.5556 1Z" stroke="#F7F7F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path className={props.crossLineClassName} d="M12 8V16" stroke="#F7F7F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path className={props.crossLineClassName} d="M8 12H16" stroke="#F7F7F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <defs>
    <clipPath id="clip0_396_230">
    <rect width="24" height="24" fill="white"/>
    </clipPath>
    </defs>
    </svg>        
};

export default New;