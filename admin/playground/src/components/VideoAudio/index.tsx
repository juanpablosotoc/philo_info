import React, { useEffect } from "react";
import { Word, Line } from '../../utils';

export default function VideoAudio(props: React.PropsWithChildren<{}>) {
    const [audioSrc, setAudioSrc] = React.useState<string | null>(null);
    const [transcript, setTranscript] = React.useState<Array<Word> | null>(null);
    useEffect(()=>{
        // make sure that all children are only text
        const children = React.Children.toArray(props.children);
        for (const child of children) {
            if (typeof child !== 'string') {
                throw new Error('VideoAudio component can only contain text');
            }
        }
        const text = children.join('');
        // get the audio src and transcript from the text
    }, [])
    return (
        <></>
    );
}