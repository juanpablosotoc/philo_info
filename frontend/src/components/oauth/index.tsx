import { PropsWithChildren, useEffect } from 'react';
import styles from './index.module.css';
import google from '../../SVG/brands/google.svg';
import apple from '../../SVG/brands/apple.svg';
import microsoft from '../../SVG/brands/microsoft.svg';
import { useGoogleLogin } from '@react-oauth/google';
import MicrosoftLogin from "react-microsoft-login";
import { saveOAuth } from '../../utils/http';
import { useNavigate } from 'react-router-dom';
import { OAuthProvider } from '../../utils/types';
import Chevron from '../chevron';

type Props = PropsWithChildren<{
    className?: string;
    type: OAuthProvider;
}>


function OAuth(props: Props) {
    const brandLogos = {'microsoft': microsoft, 'apple': apple, 'google': google};
    const brandLogo = brandLogos[props.type];
    const navigate = useNavigate();
    const googleLogin = useGoogleLogin({
    onSuccess: tokenResponse => {
        saveOAuth("google", tokenResponse.access_token);
        navigate("/");
    },
    onError: error => console.error(error),
    });
    const microsoftLogin = (err: any, data: any) => {
        if (data) {
            saveOAuth("microsoft", data.accessToken);
            navigate("/");
        }
        console.error(err);
    };
    const innerJsx = (
        <>
        <img src={brandLogo} alt={`${props.type} logo`} className={styles.brandIcon} />
        <div className={styles.wrapper}>
            <p className={styles.label}>Continue with <span className={styles.capitalize}>{props.type}</span></p>
            <hr className={styles.underline}/>
        </div>
        <Chevron className={styles.chevron} stemClassName={styles.chevronStem}/>
        </>
        )
    const cardClasses = {'apple': styles.apple, 'google': styles.google, 'microsoft': styles.microsoft};
    return (
        <div className={styles.card + ' ' + cardClasses[props.type]} onClick={()=>{
            if (props.type === "google") googleLogin();
        }}>
        {props.type === "microsoft" ? <MicrosoftLogin redirectUri={'http://localhost:3000/oauth'} clientId={'f43caeb8-61e5-4a23-89f6-a06c4677ad15'} authCallback={microsoftLogin}>
            {innerJsx}
        </MicrosoftLogin> : innerJsx}
        </div>
    );
}

export default OAuth;
