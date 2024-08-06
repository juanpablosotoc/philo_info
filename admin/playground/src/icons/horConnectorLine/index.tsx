
interface Props {
    color: 'primary' | 'secondary'
}

export default function HorConnectorLine(props: Props) {
    return (
        <svg width="485" height="77" viewBox="0 0 485 77" fill="none" xmlns="http://www.w3.org/2000/svg">
<g clip-path="url(#clip0_740_199)">
<path d="M225 17.56C225 7.86 232.86 0 242.56 0C252.26 0 260.12 7.86 260.12 17.56C260.12 27.26 252.26 35.12 242.56 35.12C232.86 35.12 225 27.26 225 17.56Z" fill="url(#paint0_radial_740_199)"/>
<path d="M0 75.5H33.52C61.01 75.5 87.48 65.15 107.68 46.5C127.87 27.85 154.35 17.5 181.84 17.5H301.67C329.46 17.5 356.25 27.84 376.83 46.5C397.41 65.16 424.21 75.5 451.99 75.5H485" stroke="url(#paint1_linear_740_199)" stroke-width="2"/>
<path d="M237 17.56C237 14.49 239.49 12 242.56 12C245.63 12 248.12 14.49 248.12 17.56C248.12 20.63 245.63 23.12 242.56 23.12C239.49 23.12 237 20.63 237 17.56Z" fill="#F7F7F7"/>
<path d="M239.5 17.56C239.5 15.87 240.87 14.5 242.56 14.5C244.25 14.5 245.62 15.87 245.62 17.56C245.62 19.25 244.25 20.62 242.56 20.62C240.87 20.62 239.5 19.25 239.5 17.56Z" fill="#101012"/>
</g>
<defs>
<radialGradient id="paint0_radial_740_199" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(242.56 17.56) rotate(-90) scale(17.56 17.56)">
<stop offset="0.35" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'}/>
<stop offset="0.4" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.84"/>
<stop offset="0.49" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.62"/>
<stop offset="0.58" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.43"/>
<stop offset="0.66" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.27"/>
<stop offset="0.75" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.15"/>
<stop offset="0.84" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.07"/>
<stop offset="0.92" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.02"/>
<stop offset="1" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0"/>
</radialGradient>
<linearGradient id="paint1_linear_740_199" x1="242.5" y1="76.5" x2="242.5" y2="16.5" gradientUnits="userSpaceOnUse">
<stop stop-color="white" stop-opacity="0"/>
<stop offset="1" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'}/>
</linearGradient>
<clipPath id="clip0_740_199">
<rect width="485" height="76.5" fill="white"/>
</clipPath>
</defs>
</svg>
    )
};