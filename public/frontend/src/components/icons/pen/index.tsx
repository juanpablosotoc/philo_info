import styles from './styles.module.css';


function Pen () {
    return <svg className={styles.icon} width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 2.00006C16.2626 1.73741 16.5744 1.52907 16.9176 1.38693C17.2608 1.24479 17.6286 1.17163 18 1.17163C18.3714 1.17163 18.7392 1.24479 19.0824 1.38693C19.4256 1.52907 19.7374 1.73741 20 2.00006C20.2626 2.2627 20.471 2.57451 20.6131 2.91767C20.7553 3.26083 20.8284 3.62862 20.8284 4.00006C20.8284 4.37149 20.7553 4.73929 20.6131 5.08245C20.471 5.42561 20.2626 5.73741 20 6.00006L6.5 19.5001L1 21.0001L2.5 15.5001L16 2.00006Z" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>    
};


export default Pen;