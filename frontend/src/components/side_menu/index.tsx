import { Link } from 'react-router-dom';
import Home from '../icons/home';
import Threads from '../threads';
import styles from './index.module.css';
import Logo from '../icons/logo';
import New from '../icons/new';
import Group from '../icons/group';
import Education from '../icons/education';
import Book from '../icons/book';
import { useState } from 'react';
import { navOptions } from '../../utils/types';
import Bars from '../icons/bars';

interface Props {
    type: 'threads';
    data: any;
    myRef?: React.RefObject<HTMLDivElement>;
    active: navOptions;
    className?: string;
}

function SideMenu(props: Props) {
    return (
        <div className={styles.wrapper + ' ' + (props.className ? props.className : '')} ref={props.myRef ? props.myRef : undefined}>
            <div className={styles.innerWrapper}>
                <div className={styles.generalWrapper}>
                    <nav>
                        <Link to='/'  className={styles.link + ' ' + styles.active}>
                            <div className={styles.iconWrapper}>
                                <Logo className={styles.logo} innerHoleClassName={styles.logoInnerHole}></Logo>
                            </div>
                            <span>FacTic</span>
                        </Link>
                        <div>
                            <Link to="/" className={`${styles.link} ${props.active === 'home' ? styles.active : ''}`}>
                                <div className={styles.iconWrapper}>
                                    <Home className={styles.home}/>
                                </div>
                                <span>Home</span>
                            </Link>
                            <Link to='/create' className={`${styles.link} ${props.active === 'new' ? styles.active : ''}`}>
                                <div className={styles.iconWrapper}>
                                    <New className={styles.new} crossLineClassName={styles.crossLine}/>
                                </div>  
                                <span>Create</span>
                            </Link>
                            <Link to='/classrooms' className={`${styles.link} ${props.active === 'group' ? styles.active : ''}`}>
                                <div className={styles.iconWrapper}>
                                    <Group className={styles.group} />
                                </div>  
                                <span>Classrooms</span>
                            </Link>
                            <Link to='/courses' className={`${styles.link} ${props.active === 'education' ? styles.active : ''}`}>
                                <div className={styles.iconWrapper}>
                                    <Education className={styles.education} holeClassName={styles.educationHole}/>
                                </div>  
                                <span>Courses</span>
                            </Link>
                            <Link to='/books' className={`${styles.link} ${props.active === 'book' ? styles.active : ''}`}>
                                <div className={styles.iconWrapper}>
                                    <Book className={styles.book}/>
                                </div>  
                                <span>Books</span>
                            </Link>
                        </div>
                        <button onClick={()=>{alert('siu')}} className={styles.moreBtn + ' ' + styles.link}>
                            <div className={styles.iconWrapper}>
                                <Bars></Bars>
                            </div>  
                            <span>More</span>
                        </button>
                    </nav>
                </div>
                {props.type === 'threads' ? <Threads threads={props.data} className={styles.specificWrapper}></Threads> : undefined}
            </div>
        </div>
    )
};

export default SideMenu;
