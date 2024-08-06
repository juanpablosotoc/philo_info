import Backward from '../../icons/backward';
import Forward from '../../icons/forward';
import Pause from '../../icons/pause';
import Play from '../../icons/play';
import styles from './styles.module.css';
import React, { useState, useEffect, useRef } from 'react';


interface AudioProps {
    src: string;
    transcript: Array<Word>;
    title: string;
}

interface Word {
    word: string;
    start: number;
    end: number;
}

interface Line {
    text: string;
    start?: number;
    end?: number;
    wordCount: number;
}


export default function Audio({ src, transcript, title }: AudioProps) {
    const wrapperRef = useRef<HTMLDivElement>(null);
    const [currentTime, setCurrentTime] = useState(0);
    const [currentLineIndex, setCurrentLineIndex] = useState<number | null>(null);
    const [duration, setDuration] = useState<number>(0);
    const linesContainerRef = useRef<HTMLParagraphElement>(null);
    const audioRef = useRef<HTMLAudioElement>(null);
    const lines: Array<Line> = [];
    const [currentPlayState, setCurrentPlayState] = useState<'playing' | 'paused'>('paused');
    const [followingLine, setFollowingLine] = useState<boolean>(true);
    let currentLine: Line = { wordCount: 0, text: '' };
    let prevWordEndTime = null;
    const [currentPlaybackSpeed, setCurrentPlaybackSpeed] = useState<string>('normal');
    for (let word of transcript) {
        if (currentLine.wordCount === 0) {
            currentLine.start = word.start;
        } else if (prevWordEndTime !== null && word.start - prevWordEndTime > 0.2) {
            currentLine.end = prevWordEndTime;
            lines.push(currentLine);
            currentLine = { wordCount: 0, text: '', start: word.start };
        }
        
        currentLine.wordCount++;
        currentLine.text += word.word + ' ';
        prevWordEndTime = word.end;

        if (currentLine.wordCount >= 8) {
            currentLine.end = word.end;
            lines.push(currentLine);
            currentLine = { wordCount: 0, text: '' };
        }
    }

    if (currentLine.wordCount > 0) {
        currentLine.end = prevWordEndTime!;
        lines.push(currentLine);
    }
    useEffect(() => {
        const audio = audioRef.current;
        const updateTime = () => {
            // get the current play percentage
            const playPerc = (audio!.currentTime / audio!.duration) * 100;
            document.body.style.setProperty('--value', `${playPerc}%`)
            setCurrentTime(audio!.currentTime);
        };
        const updateDuration = () => {
            const audioDuration = audio!.duration;
            setDuration(audioDuration);
        };

        audio!.addEventListener('timeupdate', updateTime);
        audio!.addEventListener('loadedmetadata', updateDuration);

        return () => {
            audio!.removeEventListener('timeupdate', updateTime);
            audio!.removeEventListener('loadedmetadata', updateDuration);
        };
    }, []);
    const handleSeek = (e: any) => {
        const audio = audioRef.current;
        const seekTime = (e.target.value / 100) * duration;
        audio!.currentTime = seekTime;
        // set the value css proper
        // get the current play percentage
        const playPerc = (audio!.currentTime / duration) * 100;
        wrapperRef.current!.style.setProperty('--value', `${playPerc}%`)
        setCurrentTime(seekTime);
    };

    const formatTime = (time: number) => {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60).toString().padStart(2, '0');
        return `${minutes}:${seconds}`;
    };

    function handleLineClick(start: number) {
        setFollowingLine(true);
        const audio = audioRef.current;
        audio!.currentTime = start;
        setCurrentTime(start);
    }
    useEffect(() => {
        for (let i = 0; i < lines.length; i++) {
            if (currentTime >= lines[i].start! && currentTime <= lines[i].end!) {
                setCurrentLineIndex(i);
                if (followingLine) {
                    // bring the span that is currently being played into view
                    const container = linesContainerRef.current;
                    const lineElement = container?.children[i] as HTMLElement;
                    if (lineElement && container) {
                        const lineTop = lineElement.offsetTop - container.offsetTop;
                        const lineHeight = lineElement.offsetHeight;
                        const containerHeight = container.clientHeight;
                        const scrollPosition = lineTop - (containerHeight / 2) + (lineHeight / 2);
    
                        container.scrollTo({
                            top: scrollPosition,
                            behavior: 'smooth'
                        });
                    }
                }
                break;
            }
        }
    }, [currentTime, lines]);
    

    const transcriptSpans = lines.map((line, index) => (
        <span key={index} className={index === currentLineIndex ? styles.highlight : (index < (currentLineIndex || 0) ? (styles.alreadyPassed) : '')} onClick={(e)=>{handleLineClick(line.start!)}}>
            {line.text}
        </span>
    ))
    const handleScroll = (e: React.UIEvent<HTMLParagraphElement, UIEvent>) => {
        const element = e.currentTarget;
        const currentLineElement = linesContainerRef.current?.children[currentLineIndex || 0];

        if (currentLineElement) {
            const currentLineRect = currentLineElement.getBoundingClientRect();
            const containerRect = element.getBoundingClientRect();

            // Check if current line is visible within the container
            if (
                currentLineRect.top >= containerRect.top &&
                currentLineRect.bottom <= containerRect.bottom
            ) {
                setFollowingLine(true);
            } else {
                setFollowingLine(false);
            }
        }
    };
    function forwardNSeconds(n: number = 5) {
        setCurrentTime((prevTime) => {
            const newTime = prevTime + n;
            const audio = audioRef.current;
            if (audio) {
                audio.currentTime = newTime;
            }
            return newTime;
        });
    }
    
    function backwardNSeconds(n: number = 5) {
        setCurrentTime((prevTime) => {
            const newTime = prevTime - n;
            const audio = audioRef.current;
            if (audio) {
                audio.currentTime = newTime;
            }
            return newTime;
        });
    }
    
    return (
        <div className={styles.wrapper} ref={wrapperRef}>
            <div className={styles.content}>
            <p className={styles.transcript} onScroll={handleScroll} ref={linesContainerRef}>
                <div className={styles.titleWrapper}>
                    <p className={styles.title}>{title}</p>
                    <select>
                        <option>Alloy</option>
                        <option>Echo</option>
                        <option>Fable</option>
                        <option>Onyx</option>
                        <option>Nova</option>
                        <option>Shimmer</option>
                    </select>
                </div>
                {transcriptSpans}
            </p>
            <div className={styles.innerWrapper}>
                <div className={styles.buttons}>
                    <button onClick={(e)=>backwardNSeconds()}>
                        <Backward className={styles.forwardBackward}></Backward>
                    </button>
                    <button className={styles.playPause} onClick={(e)=>{
                        audioRef.current!.paused ? audioRef.current!.play() : audioRef.current!.pause();
                    }}>
                        <Play className={currentPlayState === 'playing' ? '' : styles.active}></Play>
                        <Pause className={currentPlayState === 'paused' ? '': styles.active}></Pause>
                    </button>
                    <button onClick={(e)=>forwardNSeconds()}>
                        <Forward className={styles.forwardBackward}></Forward>
                    </button>
                </div>
                <div className={styles.sliderWrapper}>
                    <span className={styles.timeMetadata}>{formatTime(currentTime)}</span>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={(currentTime / duration) * 100 || 0}
                        onChange={handleSeek}
                        className={styles.sliderInput}
                    />
                    <span className={styles.timeMetadata}>{formatTime(duration)}</span>
                </div>
            </div>
            <audio controls ref={audioRef} hidden onPlay={()=>{setCurrentPlayState('playing')}} onPause={()=>{setCurrentPlayState('paused')}}>
                <source src={src} type="audio/mpeg" />
                Your browser does not support the audio element.
            </audio>
            </div>
            <div className={styles.playbackSpeedWrapper}>
                <div className={styles.playbackSpeedInnerWrapper}>
                <p onClick={(e)=>setCurrentPlaybackSpeed('0.5')} className={currentPlaybackSpeed === '0.5' ? styles.active : ''}>0.5</p>
                <p onClick={(e)=>setCurrentPlaybackSpeed('normal')} className={currentPlaybackSpeed === 'normal' ? styles.active : ''}>Normal</p>
                <p onClick={(e)=>setCurrentPlaybackSpeed('1.5')} className={currentPlaybackSpeed === '1.5' ? styles.active : ''}>1.5</p>
                <p onClick={(e)=>setCurrentPlaybackSpeed('2')} className={currentPlaybackSpeed === '2' ? styles.active : ''}>2</p>
                </div>
            </div>
        </div>
    );
}
