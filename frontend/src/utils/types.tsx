export type endpoint = 'users' | 'users/login' | 'users/create_user';
export type methods = "GET" | "POST" | "PUT" | "DELETE";
export interface UserState {
    email?: string;
}
export interface ErrorType {
    message?: string;
    statusText?: number;
};
export type OutputTypes = 'timeline' | 'text' | 'speech'