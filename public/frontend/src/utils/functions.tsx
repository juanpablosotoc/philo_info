import { dateComparisonString } from "./types";

function getOffset(el: any) {
    const rect = el.getBoundingClientRect();
    return {
      left: rect.left + window.scrollX,
      top: rect.top + window.scrollY
    };
}

export function getXYPercentages(e: any, element: any) {
    const mouseX = e.pageX;
    const mouseY = e.pageY;
    const {left: cardX, top: cardY} = getOffset(element);

    const cardWidth = element.offsetWidth;
    const cardHeight = element.offsetHeight;

    const x = mouseX - cardX;
    const y = mouseY - cardY;
    const xPercent = Math.trunc((x / cardWidth) * 100);
    const yPercent = Math.trunc((y / cardHeight) * 100);

    return { xPercent, yPercent };
};

export function dateComparison( d2: Date ){
    let d1 = new Date();
    let comparison = 'Older';
    if (d1.getUTCFullYear() == d2.getUTCFullYear()) {
        comparison = 'This year';
        if (d1.getUTCMonth() == d2.getUTCMonth()) {
            comparison = 'This month';
            if (d1.getUTCDate() == d2.getUTCDate()) {
                comparison = 'Today';
            }
    }};
    return comparison as dateComparisonString;
};

export function isLink(text: string) {
    return text.startsWith('http://') || text.startsWith('https://');
};
export const getFormData =(object: any)=> Object.keys(object).reduce((formData, key) => {
    formData.append(key, object[key]);
    return formData;
}, new FormData());


function cleanStr(text: string) {
    return text.replace('data: ', '');
}

export function parseStream(streamStr: string): Array<any> {
    let countedStrings = [];
    let currentStr = '';
    let openingCurlyBraces = 0;
    let closingCurlyBraces = 0;
    let prevCharWasEscBackslash = false;
    let insideOfString = false;

    streamStr = streamStr.replace("data:", "");

    for (let i = 0; i < streamStr.length; i++) {
        let char = streamStr[i];
        currentStr += char;
        
        if (insideOfString) {
            if (prevCharWasEscBackslash) {
                prevCharWasEscBackslash = false;
                continue;
            } else {
                if (char === '\\') {
                    prevCharWasEscBackslash = true;
                } else if (char === '"') {
                    insideOfString = false;
                }
            }
        } else {
            if (openingCurlyBraces > 0 && openingCurlyBraces === closingCurlyBraces) {
                countedStrings.push({ complete: true, data: cleanStr(currentStr) });
                currentStr = '';
                openingCurlyBraces = 0;
                closingCurlyBraces = 0;
            }
            if (char === '"') {
                insideOfString = true;
            } else if (char === '{') {
                openingCurlyBraces += 1;
            } else if (char === '}') {
                closingCurlyBraces += 1;
            }
        }
    }

    if (currentStr.length > 0) {
        if (openingCurlyBraces === closingCurlyBraces) {
            countedStrings.push({ complete: true, data: cleanStr(currentStr) });
        } else {
            countedStrings.push({ complete: false, data: cleanStr(currentStr) });
        }
    }

    let actualResp = [];
    for (let item of countedStrings) {
        if (item.complete) {
            actualResp.push(JSON.parse(item.data));
        } else {
            actualResp.push(item.data);
        }
    }

    return actualResp;
}