import { PropsWithChildren } from 'react';
import styles from './index.module.css';
import google_black from '../../SVG/brands/google_black.svg';
import google_grey from '../../SVG/brands/google_grey.svg';
import apple_black from '../../SVG/brands/apple_black.svg';
import apple_grey from '../../SVG/brands/apple_grey.svg';
import microsoft_black from '../../SVG/brands/microsoft_black.svg';
import microsoft_grey from '../../SVG/brands/microsoft_grey.svg';

type Props = PropsWithChildren<{
    className?: string;
    type: "apple" | "microsoft" | "google";
}>


function OAuth(props: Props) {
    const brandLogo = {'grey': '', 'black': ''}
    if (props.type === "apple") {
        brandLogo['grey'] = apple_grey;
        brandLogo['black'] = apple_black;
    }
    else if (props.type === "google") {
        brandLogo['black'] = google_black;
        brandLogo['grey'] = google_grey;
    }
    else {
        brandLogo['grey'] = microsoft_grey;
        brandLogo['black'] = microsoft_black;
    };
    return (
        <div className={styles.card}>
            <div className={styles.brandDiv}>
                <img src={brandLogo['grey']} alt={`${props.type} logo`} className={styles.greyBrand}/>
                <img src={brandLogo['black']} alt={`${props.type} logo`} className={styles.blackBrand} />
            </div>
            <p className={styles.label}>Continue with <span className={styles.capitalize}>{props.type}</span></p>
        </div>
    );
}

export default OAuth;
