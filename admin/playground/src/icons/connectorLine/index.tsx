interface Props {
    color: 'primary' | 'secondary'
}

export default function ConnectorLine(props: Props) {
    return (
<svg width="77" height="485" viewBox="0 0 77 485" fill="none" xmlns="http://www.w3.org/2000/svg">
<g clip-path="url(#clip0_731_194)">
<path d="M58.94 225C68.64 225 76.5 232.86 76.5 242.56C76.5 252.26 68.64 260.12 58.94 260.12C49.24 260.12 41.38 252.26 41.38 242.56C41.38 232.86 49.24 225 58.94 225Z" fill="url(#paint0_radial_731_194)"/>
<path d="M1 0V33.52C1 61.01 11.35 87.48 30 107.68C48.65 127.87 59 154.35 59 181.84V301.67C59 329.46 48.66 356.25 30 376.83C11.34 397.41 1 424.21 1 451.99V485" stroke="url(#paint1_linear_731_194)" stroke-width="2"/>
<path d="M58.94 237C62.01 237 64.5 239.49 64.5 242.56C64.5 245.63 62.01 248.12 58.94 248.12C55.87 248.12 53.38 245.63 53.38 242.56C53.38 239.49 55.87 237 58.94 237Z" fill="#F7F7F7"/>
<path d="M58.94 239.5C60.63 239.5 62 240.87 62 242.56C62 244.25 60.63 245.62 58.94 245.62C57.25 245.62 55.88 244.25 55.88 242.56C55.88 240.87 57.25 239.5 58.94 239.5Z" fill="#101012"/>
</g>
<defs>
<radialGradient id="paint0_radial_731_194" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(58.94 242.56) scale(17.56 17.56)">
<stop offset="0.35" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'}/>
<stop offset="0.4" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.84"/>
<stop offset="0.49" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.62"/>
<stop offset="0.58" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.43"/>
<stop offset="0.66" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.27"/>
<stop offset="0.75" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.15"/>
<stop offset="0.84" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0.07"/>
<stop offset="0.92" stop-color="#F2055D" stop-opacity="0.02"/>
<stop offset="1" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'} stop-opacity="0"/>
</radialGradient>
<linearGradient id="paint1_linear_731_194" x1="-8.09287e-08" y1="242.5" x2="60" y2="242.5" gradientUnits="userSpaceOnUse">
<stop stop-color="white" stop-opacity="0"/>
<stop offset="1" stop-color={props.color === 'primary' ? "#F2055D" : '#05F3DB'}/>
</linearGradient>
<clipPath id="clip0_731_194">
<rect width="76.5" height="485" fill="white"/>
</clipPath>
</defs>
</svg>

    )
};
