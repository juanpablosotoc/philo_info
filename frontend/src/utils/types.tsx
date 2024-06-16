export type endpoint = 'users/' | 'users/login' | 'users/create_user' |
 'topics/' | 'threads/' | 'threads/message' | 'oauth/login_create_account' |
 'mixed/topics_threads';
export type methods = "GET" | "POST" | "PUT" | "DELETE";
export type OAuthProvider = 'google' | 'apple' | 'microsoft';
export type BearerType = 'alt_token' | 'access_token';
export interface UserState {
    email?: string;
}
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
export type Thread = {
    id: number;
    name: string;
    date: Date;
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
export type choice = Array<OutputTypes>
export type choicesType = choice[]
export type contentType = "application/json" | "multipart/form-data"
export class InformationBundleCls {
    constructor(public texts: Array<string>, public files: Array<File>, public links: Array<string>) {}
}
export class QuestionCls {
    question: string;
    constructor(question: string, public topic: string) {
        question = question.trim();
        if (!question.length || !question.startsWith('/explain')) throw new Error("Invalid question");
        this.question = question;
    }
};

export class MessageCls {
    constructor(public content: InformationBundleCls | QuestionCls, public type: 'coices' | 'question' | 'informationBundle', public threadId?: number) {}
}
