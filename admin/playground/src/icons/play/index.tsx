import styles from './styles.module.css';

interface Props {
    className?: string;
}

export default function Play (props: Props) {
    return (
        <svg className={styles.icon + ' ' + (props.className ? props.className : '')} width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M3 1.20344C2.99977 0.992316 3.05486 0.784851 3.15975 0.601922C3.26464 0.418993 3.41561 0.267052 3.59749 0.161387C3.77936 0.0557213 3.98572 5.89325e-05 4.1958 4.67705e-08C4.40588 -5.8839e-05 4.61226 0.0554877 4.7942 0.161051L23.4026 10.9593C23.5842 11.0649 23.7351 11.2166 23.8399 11.3993C23.9448 11.5819 24 11.7891 24 12C24 12.2109 23.9448 12.4181 23.8399 12.6007C23.7351 12.7834 23.5842 12.9351 23.4026 13.0407L4.7942 23.8389C4.61239 23.9444 4.40616 24 4.19622 24C3.98629 24 3.78005 23.9445 3.59823 23.839C3.4164 23.7336 3.2654 23.5819 3.16039 23.3992C3.05538 23.2165 3.00007 23.0093 3 22.7983V1.20344Z"/>
</svg>
    )
};
