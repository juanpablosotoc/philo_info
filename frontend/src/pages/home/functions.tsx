import React from "react";
import { getFormData } from "../../utils/functions";
import { post_stream } from "../../utils/http";
import {StreamMessageRequestType, StreamMessage, MessageCls, InfoMessageCls, InformationBundleCls, 
    StreamMessageResponseMetadata, StreamMessageResponseChoices, StreamMessageResponseProcessedInfo, 
    RequestMessageCls, StreamMessageResponseOther, ThreadCls} from "../../utils/types";

export default class HandleSubmitCls {
    constructor(public longTextInput: any, public setLongTextInputValue: any, public setFiles: any, public longTextInputValue: string, public files: Array<File>,
        public setMessages: React.Dispatch<React.SetStateAction<MessageCls[]>>, public setThreads: React.Dispatch<React.SetStateAction<ThreadCls[]>>) {
    }
    async handleSubmit() {
        let prevTexts: Array<string> = [];
        const prevLinks: Array<string> = [];
        for (let node of this.longTextInput.current!.childNodes) {
            // if node is span add the text content
            if (node.nodeName === 'SPAN') {
                prevLinks.push(node.textContent!);
            } else if (node.nodeName === '#text') {
                if (prevTexts.length) {
                    prevTexts[prevTexts.length - 1] = prevTexts[prevTexts.length - 1] + ' ' + node.textContent!;
                } else if (node.textContent && node.textContent.trim()){
                    prevTexts.push(node.textContent!);
                }
            }
        };
        let message = new MessageCls();
        this.setMessages((prevMessages) => {
            return [...prevMessages, message];
        });
        const prevFiles = this.files;
        const prevText = this.longTextInputValue;
        this.setLongTextInputValue('');
        this.setFiles([]);
        // Make a post request to the server
        const body_obj = {text: this.longTextInputValue}
        const body = getFormData(body_obj);
        const resp = post_stream("threads/message", true, body);
        let currentMessageType: StreamMessageRequestType | null = null;
        let setMessage = false;
        for await (let list of resp) {
            for (let item of (list as Array<StreamMessage>)) {
                // Check if request_type is in the items keys
                if ('request_type' in item) {
                    setMessage = false;
                    // Item has following structure 
                    // {request_type: 'info' | 'change_appearance' | 'quiz' | 'contact' | 'create_playlist' | 'recap' | 'other}
                    currentMessageType = item.request_type;
                    if (item.request_type === 'change_appearance') {
                        // Do something
                    }
                } else {
                    // Item has following structure
                    // {type: 'metadata' | 'choices' | 'processed_info', message_id: number, *other specific keys*}
                    if (currentMessageType === 'info') {
                        if (!setMessage) {
                            setMessage = true;
                            this.setMessages((prevMessages) => {
                                return prevMessages.map((prevMessage) => {
                                    const copyMessage = structuredClone(prevMessage);
                                    if (!copyMessage.id) {
                                        copyMessage.request_type = 'info';
                                        copyMessage.content = new InfoMessageCls(new InformationBundleCls(prevTexts, prevFiles, prevLinks));
                                        return copyMessage;
                                    }
                                    return copyMessage;
                                })
                            })
                        }
                        if (item.type === 'metadata') {
                            this.setMessages((prevMessages) => {
                                return prevMessages.map((prevMessage) => {
                                    const copyMessage = structuredClone(prevMessage);
                                    if (!copyMessage.id) {
                                        copyMessage.id = (item as StreamMessageResponseMetadata).message_id;
                                        copyMessage.threadId = (item as StreamMessageResponseMetadata).thread_id;
                                    }
                                    return copyMessage;
                                });
                            });
                            const thread = new ThreadCls(item.thread_id, item.thread_name, new Date());
                            this.setThreads((prevThreads) => {
                                return [...prevThreads, thread];
                            });
                        } else if (item.type === 'choices') {
                            this.setMessages((prevMessages) => {
                                return prevMessages.map((prevMessage) => {
                                    const copyMessage = structuredClone(prevMessage);
                                    if (copyMessage.id === (item as StreamMessageResponseChoices).message_id) {
                                        (copyMessage.content! as InfoMessageCls).possible_outputs = (item as StreamMessageResponseChoices).possible_outputs;
                                    }
                                    return copyMessage;
                            })});
                        } else {
                            // Type is processed_info
                            this.setMessages((prevMessages) => {
                                return prevMessages.map((prevMessage) => {
                                    const copyMessage = structuredClone(prevMessage);
                                    if (copyMessage.id === (item as StreamMessageResponseProcessedInfo).message_id) {
                                        (copyMessage.content! as InfoMessageCls).processedInfos.push({id: (item as StreamMessageResponseProcessedInfo).id, info: (item as StreamMessageResponseProcessedInfo).info});
                                    }
                                    return copyMessage;
                                });
                            })
                        }
                    } else if (currentMessageType === 'other') {
                        if (!setMessage) {
                            setMessage = true;
                            this.setMessages((prevMessages) => {
                                return prevMessages.map((prevMessage) => {
                                    const copyMessage = structuredClone(prevMessage);
                                    if (!copyMessage.id) {
                                        copyMessage.request_type = 'other';
                                        copyMessage.content = new RequestMessageCls(prevText, '')
                                        return copyMessage;
                                    }
                                    return copyMessage;
                                })
                            })
                        } 
                        if (item.type === 'other') {
                            this.setMessages((prevMessages) => {
                                return prevMessages.map((prevMessage) => {
                                    // Grab a copy of the previous message
                                    const copyMessage = structuredClone(prevMessage);
                                    if (!copyMessage.id) {
                                        if (!((copyMessage.content as RequestMessageCls).response)) {
                                            (copyMessage.content as RequestMessageCls).response = (item as StreamMessageResponseOther).data;
                                        } else {
                                            // prev message is already existing
                                            (copyMessage.content as RequestMessageCls).response += (item as StreamMessageResponseOther).data;
                                        }
                                        return copyMessage;
                                    }
                                    return copyMessage;
                                });
                            });
                        } else {
                            // item type is metadata
                            this.setMessages((prevMessages) => {
                                return prevMessages.map((prevMessage) => {
                                    const copyMessage = structuredClone(prevMessage);
                                    if (!copyMessage.id) {
                                        copyMessage.id = (item as StreamMessageResponseMetadata).message_id;
                                        copyMessage.threadId = (item as StreamMessageResponseMetadata).thread_id;
                                    }
                                    return copyMessage;
                                });
                            });
                        }
                    }
                }
            }
        }
    };
}