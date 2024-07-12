interface Props {
    className?: string;
    holeClassName?: string;
}

function Education (props: Props) {
    return <svg width="24" className={props.className ? props.className : ''} height="21" viewBox="0 0 24 21" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g clip-path="url(#clip0_397_236)">
    <path d="M3.34003 12.924V14.0488C3.34003 15.231 3.98278 16.3214 5.02726 16.8838L10.2726 19.7532C10.9613 20.132 11.7877 20.132 12.4763 19.7532L17.7331 16.8838C18.7661 16.3214 19.4089 15.2425 19.4089 14.0603V12.9354C19.4089 12.2353 18.6628 11.7877 18.043 12.1205L12.4763 15.1621C11.7877 15.5409 10.9613 15.5409 10.2726 15.1621L4.70588 12.1205C4.08608 11.7877 3.34003 12.2353 3.34003 12.9354V12.924ZM10.2726 0.275466L0.596843 5.55524C-0.195123 5.99139 -0.195123 7.13917 0.596843 7.57532L10.2726 12.8551C10.9613 13.2339 11.7877 13.2339 12.4763 12.8551L20.3386 8.56241C20.9584 8.22956 21.7044 8.67719 21.7044 9.37733V14.5997C21.7044 15.231 22.2209 15.7475 22.8522 15.7475C23.4835 15.7475 24 15.231 24 14.5997V7.24247C24 6.81779 23.7704 6.43902 23.4032 6.23242L12.4763 0.275466C11.7877 -0.0918221 10.9613 -0.0918221 10.2726 0.275466Z" fill="#F7F7F7"/>
    <path className={props.holeClassName ? props.holeClassName : ''} d="M11.9254 10.9498L18.7087 7.18509C19.2941 6.85224 19.3056 6.01436 18.7202 5.6815L12.0172 1.79054C11.7532 1.64133 11.4433 1.62985 11.1793 1.77906L4.0746 5.54377C3.46628 5.86515 3.4548 6.73746 4.06312 7.07031L11.0875 10.9613C11.3515 11.1105 11.6729 11.1105 11.9254 10.9613V10.9498Z" fill="#101012"/>
    </g>
    <defs>
    <clipPath id="clip0_397_236">
    <rect width="24" height="20.0287" fill="white"/>
    </clipPath>
    </defs>
    </svg>    
};


export default Education;