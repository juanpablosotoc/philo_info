interface Props {
    className?: string;
    innerHoleClassName?: string;
}

function Logo(props: Props) {
    return <svg width="462" className={props.className ? props.className : ''} height="512" viewBox="0 0 462 512" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path className={props.innerHoleClassName ? props.innerHoleClassName : ''} d="M446.079 200.766V411.151H110.176V209.842L286.04 108.994L351.979 146.851L446.079 200.766Z" fill="#F7F7F7"/>
    <path d="M351.979 100.693V146.851L286.04 108.994L110.176 209.842V365.227L85.0412 350.798L0.0957642 302.158V100.693L176.115 0L311.64 77.5758L351.979 100.693Z" fill="#05F3DB"/>
    <path d="M461.904 209.842V411.307L286.04 512L110.176 411.307V365.227L176.115 403.006L351.979 302.158V146.851L446.079 200.766L461.904 209.842Z" fill="#FF005A"/>
    </svg>    
};

export default Logo;