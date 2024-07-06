export type endpoint = 'users/' | 'users/login' | 'users/create_user' |
 'topics/' | 'threads/' | 'threads/message' | 'oauth/login_create_account' |
 'mixed/topics_threads';
export type methods = "GET" | "POST" | "PUT" | "DELETE";
export type OAuthProvider = 'google' | 'apple' | 'microsoft';
export type BearerType = 'alt_token' | 'access_token';
export type navOptions = 'home' | 'new' | 'group' | 'education' | 'book';
export interface UserState {
    email?: string;
}
export interface StreamMessageResponseMetadata {
    type: 'metadata';
    message_id: number;
    thread_id: number;
    thread_name: string;
}
export interface StreamMessageResponseChoices {
    type: 'choices';
    message_id: number;
    possible_outputs: Array<OutputTypes>;
}
export interface StreamMessageResponseProcessedInfo {
    type: 'processed_info';
    id: string;
    info: string;
    message_id: number;
}
export type StreamMessageResponse = StreamMessageResponseMetadata | StreamMessageResponseChoices | StreamMessageResponseProcessedInfo;
export interface OAuthToken {
    identity: string;
    provider: OAuthProvider;
}
export interface ErrorType {
    status: number;
    statusText?: string;
};
export type Topic = {
    topic: string;
    questions: Array<string>;
}
export class ThreadCls {
    constructor(public id: number, public name: string, public date: Date) {}
}
export interface request_obj {
    method: "GET" | "POST";
    headers: Headers;
    body: any;
}
export interface LongTextInputType {
    content: string;
    type: 'text' | 'link';
}
export type dateComparisonString = 'Today' | 'This month' | 'Older'
export type OutputTypes = 'timeline' | 'text' | 'speech'
export type contentType = "application/json" | "multipart/form-data"
export class InformationBundleCls {
    constructor(public texts: Array<string>, public files: Array<File>, public links: Array<string>, public questions: Array<string>) {}
}
export class DefaultQuestionsCls {
    question: string;
    constructor(question: string, public topic: string) {
        question = question.trim();
        if (!question.length || !question.startsWith('/explain')) throw new Error("Invalid question");
        this.question = question;
    }
};
export class ProcessedInfoTextCls {
    constructor(public content: string, public id: string) {}
}
export class ProcessedInfoCls {
    constructor(public texts: Array<ProcessedInfoTextCls>, public message_id: number) {}
}
interface processedInfo {
    id: string;
    info: string;
}
export class MessageCls {
    constructor(public content: InformationBundleCls, public id?: number , 
        public threadId?: number, public possible_outputs?: Array<OutputTypes>,
        public processedInfos: Array<processedInfo> = []
        ) {}
}
