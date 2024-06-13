import { useEffect, useState } from "react";
import type { BearerType, Thread, Topic, choicesType, contentType, endpoint, methods } from "./types";
import { fetch_, getOAuth, getToken, saveToken } from "./http";
import { clearOAuth, post} from "./http";

function useFetch(
    endpoint: endpoint, 
    auth: boolean = false,
    method: methods,
    type: contentType,
    bearer?: BearerType,
    body?: BodyInit,
    ) {
    const [data, setData] = useState<any>();
    const [error, setError] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    useEffect(() => {
        fetch_(endpoint, auth, method, type,bearer, 
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
    const {data, isLoading, error} = useFetch("threads/message", true, "POST", "multipart/form-data","alt_token", JSON.stringify(body));
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

