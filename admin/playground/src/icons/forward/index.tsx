interface Props {
    className?: string;
}

export default function Forward(props: Props) {
    return (
        <svg className={props.className ? props.className : ''} width="21" height="24" viewBox="0 0 21 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M10.0844 24C12.8748 24 15.2522 23.0166 17.2189 21.05C18.7556 19.5133 19.6921 17.7254 20.0284 15.6843C20.1816 14.7584 19.4707 13.9155 18.5321 13.9155C17.7872 13.9155 17.1635 14.4604 17.038 15.1947C16.7676 16.7761 15.9759 18.1426 14.6648 19.2919C13.5559 20.2646 12.1469 20.8542 10.6761 20.9542C8.51366 21.1032 6.68322 20.4498 5.18482 18.9982C3.80986 17.6658 3.02235 15.8183 3.02661 13.9028C3.02873 11.9233 3.74388 10.2398 5.16779 8.84991C6.49805 7.55158 8.30294 6.85559 10.1611 6.85559C10.1887 6.85559 10.2036 6.88964 10.1845 6.9088L8.68393 8.43913C8.17311 8.96059 8.17311 9.7928 8.68393 10.3143L8.93721 10.5739C9.45867 11.1082 10.3164 11.1124 10.8443 10.5846L14.9883 6.44055C15.5119 5.91696 15.5119 5.06772 14.9883 4.54413L10.8294 0.391594C10.3058 -0.131996 9.45655 -0.131996 8.93296 0.391594L8.66052 0.664031C8.13693 1.18762 8.13693 2.03686 8.66052 2.56045L9.8801 3.78003C9.89925 3.79919 9.88648 3.83111 9.85882 3.83324C7.13444 3.91625 4.81234 4.92299 2.89677 6.85559C0.9663 8.80734 0 11.1592 0 13.9155C0 16.6718 0.983327 19.0833 2.94998 21.05C4.91664 23.0166 7.29408 24 10.0844 24Z" fill="black"/>
</svg>
    )
};