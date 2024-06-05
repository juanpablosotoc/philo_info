import { useEffect, useState } from "react";
import type { Thread, choicesType, contentType, endpoint, methods } from "./types";
import { fetch_ } from "./http";

function useFetch(
    endpoint: endpoint, 
    auth: boolean = false,
    method: methods,
    type: contentType,
    body?: BodyInit,
    ) {
    const [data, setData] = useState<any>();
    const [error, setError] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    useEffect(() => {
        fetch_(endpoint, auth, method, type, 
            (jsonResp) => {setData(jsonResp)}, 
            (e) => {setError(true)}, 
            () => {setIsLoading(false)}, 
            body)
    }, []);
    return {
      data,
      error,
      isLoading,
    };
}

export function useThreads() {
    const [threads, setThreads] = useState<Thread[]>([]);
    const {data, isLoading, error} = useFetch("threads/", true, "GET", "application/json");
    useEffect(() => {
        if (data && !error) {
            const listOfThreads = data.threads.map((thread: any) => {
                return {
                    id: thread.id,
                    name: thread.name,
                    date: new Date(thread.date)
                }
            })
            setThreads(listOfThreads);
        }
     }, [data]);
    return {
        threads,
        isLoading,
        error
    };
}

export function useMessage(message: string, files: File[] | undefined, threadId?: number) {
    const [choices, setChoices] = useState<choicesType>([]);
    const texts = [];
    const links = [];
    if (message.startsWith("http")) {
        links.push(message);
    } else {
        texts.push(message);
    }
    const body = {
        texts,
        links,
        files,
        threadId
    }
    type response = {
        choices: choicesType
    }
    const {data, isLoading, error} = useFetch("threads/message", true, "POST", "multipart/form-data", JSON.stringify(body));
    useEffect(() => {
        if (data) {
            setChoices((data as response).choices);
        }
     }, [data]);
    return {
        choices,
        isLoading,
        error
    };
};