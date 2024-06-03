export type endpoint = 'users/' | 'users/login' | 'users/create_user' | 'topics/';
export type methods = "GET" | "POST" | "PUT" | "DELETE";
export interface UserState {
    email?: string;
}
export interface ErrorType {
    status: number;
    statusText?: string;
};
export type OutputTypes = 'timeline' | 'text' | 'speech'
export type Topic = {
    topic: string;
    questions: Array<string>;
}